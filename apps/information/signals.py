from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.authuser.models import StudentDetail
from apps.information.models import Notice
from apps.routine.signals import send_sms, send_email
from apps.routine.utils import get_batch

User = get_user_model()


@receiver(post_save, sender=Notice)
def send_notice_notification(sender, instance, *args, **kwargs):
    eligible_students = StudentDetail.objects.filter(programme=instance.programme, is_class_representative=True)
    eligible_students = [student for student in eligible_students if
                         student.current_year == instance.year and student.current_part == instance.part]
    phone_numbers = [student.phone for student in eligible_students]
    emails = [student.email for student in eligible_students]
    names = [student.user.get_full_name() for student in eligible_students]
    names = ', '.join(names)
    if instance.send_sms:
        send_sms(phone_numbers, instance.message, instance.notice_by.get_full_name())
    if instance.send_email:
        # send email
        context = {
            'notice': instance
        }
        send_email('Notice from %s' % (names,), 'information/notice.html', context, emails)


@receiver(pre_save, sender=Notice)
def manage_batch(sender, instance, *args, **kwargs):
    instance.batch = get_batch(instance.year, instance.part)
