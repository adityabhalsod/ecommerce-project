from config.celery import app
from django.utils import timezone
from django.db.models import Q

from v1.membership.models import Membership


@app.task
def set_automatically_deactivate_membership():
    query_filter = Q()
    query_filter.add(Q(start_at__lte=timezone.now(), end_at__gte=timezone.now()), Q.AND)
    query_filter.add(Q(is_active=True), Q.AND)

    memberships = Membership.objects.exclude(query_filter, is_active=False)
    for membership in memberships:
        membership.is_active = False
        membership.save()

    print("----------------------set_automatically_deactivate_membership")
    return True
