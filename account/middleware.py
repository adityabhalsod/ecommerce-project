import traceback
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.db.utils import DatabaseError
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import NotFound

from account import utils
from account.ip import get_client_ip
from account.models import BannedIP, UntrackedUserAgent, Visitor


class VisitorTrackingMiddleware(MiddlewareMixin):
    """
    Keeps track of your active users.  Anytime a visitor accesses a valid URL,
    their unique record will be updated with the page they're on and the last
    time they requested a page.

    Records are considered to be unique when the session key and IP address
    are unique together.  Sometimes the same user used to have two different
    records, so I added a check to see if the session key had changed for the
    same IP and user agent in the last 5 minutes
    """

    @property
    def prefixes(self):
        """Returns a list of URL prefixes that we should not track"""

        if not hasattr(self, "_prefixes"):
            self._prefixes = getattr(settings, "NO_TRACKING_PREFIXES", [])

            if not getattr(settings, "_FREEZE_TRACKING_PREFIXES", False):
                for name in ("MEDIA_URL", "STATIC_URL"):
                    url = getattr(settings, name)
                    if url and url != "/":
                        self._prefixes.append(url)

                settings.NO_TRACKING_PREFIXES = self._prefixes
                settings._FREEZE_TRACKING_PREFIXES = True

        return self._prefixes

    def process_request(self, request):
        # create some useful variables
        ip_address, _ = get_client_ip(request)
        user_agent = str(request.META.get("HTTP_USER_AGENT", ""))[:255]

        # retrieve untracked user agents from cache
        ua_key = "_tracking_untracked_uas"
        untracked = cache.get(ua_key)
        if untracked is None:
            untracked = UntrackedUserAgent.objects.all()
            cache.set(ua_key, untracked, 3600)

        # see if the user agent is not supposed to be tracked
        for ua in untracked:
            # if the keyword is found in the user agent, stop tracking
            if user_agent.find(ua.keyword) != -1:
                print(
                    'Not tracking UA "%s" because of keyword: %s'
                    % (user_agent, ua.keyword)
                )
                return

        if hasattr(request, "session") and request.session.session_key:
            # use the current session key if we can
            session_key = request.session.session_key
        else:
            # otherwise just fake a session key
            session_key = "%s:%s" % (ip_address, user_agent)
            session_key = session_key[:40]

        # ensure that the request.path does not begin with any of the prefixes
        for prefix in self.prefixes:
            if request.path.startswith(prefix):
                print("Not tracking request to: %s" % request.path)
                return

        # if we get here, the URL needs to be tracked
        # determine what time it is

        attrs = {"session_key": session_key, "ip_address": ip_address}

        # for some reason, Visitor.objects.get_or_create was not working here
        try:
            visitor = Visitor.objects.get(**attrs)
        except Visitor.DoesNotExist:
            # see if there's a visitor with the same IP and user agent
            # within the last 5 minutes
            cutoff = timezone.now() - timedelta(minutes=5)
            visitors = Visitor.objects.filter(
                ip_address=ip_address, user_agent=user_agent, last_update__gte=cutoff
            )

            if len(visitors):
                visitor = visitors[0]
                visitor.session_key = session_key
                print(
                    "Using existing visitor for IP %s / UA %s: %s"
                    % (ip_address, user_agent, visitor.id)
                )
            else:
                # it's probably safe to assume that the visitor is brand new
                visitor = Visitor(**attrs)
                print("Created a new visitor: %s" % attrs)
        except:
            return

        # determine whether or not the user is logged in
        user = request.user
        if isinstance(user, AnonymousUser):
            user = None

        # update the tracking information
        visitor.user = user
        visitor.user_agent = user_agent

        # if the visitor record is new, or the visitor hasn't been here for
        # at least an hour, update their referrer URL
        one_hour_ago = timezone.now() - timedelta(hours=1)
        if not visitor.last_update or visitor.last_update <= one_hour_ago:
            visitor.referrer = utils.u_clean(
                request.META.get("HTTP_REFERER", "unknown")[:255]
            )

            # reset the number of pages they've been to
            visitor.page_views = 0
            visitor.session_start = timezone.now()

        visitor.url = request.path
        visitor.page_views += 1
        visitor.last_update = timezone.now()
        try:
            visitor.save()
        except DatabaseError:
            print(
                "There was a problem saving visitor information:\n%s\n\n%s"
                % (traceback.format_exc(), locals())
            )


class VisitorCleanUpMiddleware(MiddlewareMixin):
    """Clean up old visitor tracking records in the database"""

    def process_request(self, request):
        timeout = utils.get_cleanup_timeout()

        if str(timeout).isdigit():
            timeout = timezone.now() - timedelta(hours=int(timeout))
            Visitor.objects.filter(last_update__lte=timeout).delete()


class BannedIPMiddleware(MiddlewareMixin):
    """
    Raises an Http404 error for any page request from a banned IP.  IP addresses
    may be added to the list of banned IPs via the Django admin.

    The banned users do not actually receive the 404 error--instead they get
    an "Internal Server Error", effectively eliminating any access to the site.
    """

    def process_request(self, request):
        key = "_tracking_banned_ips"
        ips = cache.get(key)
        if ips is None:
            # compile a list of all banned IP addresses
            ips = [b.ip_address for b in BannedIP.objects.all()]
            cache.set(key, ips, 3600)

        # check to see if the current user's IP address is in that list
        ip_address, _ = get_client_ip(request)
        if ip_address in ips:
            raise NotFound(detail="This ip are not found!")
