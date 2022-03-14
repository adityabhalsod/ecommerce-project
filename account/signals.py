from datetime import datetime
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from account.choice import SystemDefaultGroup
from account.models import BannedIP, UntrackedUserAgent, User
from v1.wallet.tasks import customer_wallet

signals_type = (
    post_save,
    post_delete,
)


@receiver(signals_type, sender=UntrackedUserAgent)
def refresh_untracked_user_agents(sender, instance, created=False, **kwargs):
    """Updates the cache of user agents that we don't track"""

    print("Updating untracked user agents cache")
    cache.set("_tracking_untracked_uas", UntrackedUserAgent.objects.all(), 3600)


@receiver(signals_type, sender=BannedIP)
def refresh_banned_ips(sender, instance, created=False, **kwargs):
    """Updates the cache of banned IP addresses"""

    print("Updating banned IP cache")
    cache.set(
        "_tracking_banned_ips", [b.ip_address for b in BannedIP.objects.all()], 3600
    )


@receiver(post_save, sender=User)
def initialization_customer_wallet(sender, instance, created=False, **kwargs):
    if instance and instance.is_profile_completely_filled:
        if hasattr(instance, "groups") and instance.groups:
            if instance.groups.filter(name=SystemDefaultGroup.CUSTOMER):
                customer_wallet.delay(instance)
    return True


@receiver(pre_save, sender=User)
def generate_referral_code(sender, instance, created=False, **kwargs):
    if instance and instance.is_profile_completely_filled:
        if hasattr(instance, "groups") and instance.groups:
            if instance.groups.filter(name=SystemDefaultGroup.CUSTOMER):
                if instance.first_name and instance.last_name:
                    now = datetime.now()
                    first_name = str(instance.first_name).upper()[-2:]
                    last_name = str(instance.last_name).upper()[-2:]
                    year = str(now.year)[-2:]
                    month = "{:02d}".format(int(now.month))
                    instance.referral_code = "{}{}{}{}{}".format(
                        first_name, year, month, last_name, str(instance.pk)
                    )
    return True
