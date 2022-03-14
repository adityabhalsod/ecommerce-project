from django.db.models.signals import post_save
from django.dispatch import receiver
from account.choice import SystemDefaultGroup
from v1.delivery.models import DeliveryBoy
from v1.wallet.tasks import delivery_boy_wallet


@receiver(post_save, sender=DeliveryBoy)
def initialization_delivery_boy_wallet(sender, instance, created=False, **kwargs):
    if instance and instance.user and instance.user.is_profile_completely_filled:
        if hasattr(instance.user, "groups") and instance.user.groups:
            if instance.groups.filter(name=SystemDefaultGroup.DELIVERY_BOY):
                delivery_boy_wallet.delay(instance)
    return True
