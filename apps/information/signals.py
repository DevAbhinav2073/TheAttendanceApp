from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.information.models import Notice


@receiver(post_save, sender=Notice)
def send_notice_notification(sender, instance, *args, **kwargs):
    if instance.send_sms:
        # send sms
        pass

    if instance.send_email:
        # send email
        pass
