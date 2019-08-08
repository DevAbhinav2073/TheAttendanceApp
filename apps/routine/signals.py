import _thread
from datetime import datetime, date, timedelta

import requests
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from apps.authuser.models import StudentDetail
from apps.routine.models import ClassAttendingDetail, SMSCredit


def send_email(subject, template, context, to_emails):
    to_emails = ['theabhinavdev@gmail.com', ]
    from_email = 'classinfo@no-reply.com'
    html_content = render_to_string(template_name=template, context=context)  # render with dynamic value
    text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.

    # create the email, and attach the HTML version as well.
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_sms(number, text, footnote):
    # return
    if not SMSCredit.has_credit():
        return
    url = "http://api.sparrowsms.com/v2/sms/"
    message = '%s - %s' % (text, footnote)
    querystring = {"token": "SpjwPldIkL6WuzQRb2MJ", "from": "InfoSMS", "to": number,
                   "text": message}

    payload = ""
    headers = {
        'cache-control': "no-cache",
        'Postman-Token': "69dcd7a6-2327-49a7-9ee5-acb4dcd95344"
    }
    # print(message)
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    credit_used = response.json().get('credit_consumed')
    SMSCredit.deduct_credit(credit_used)


@receiver(pre_save, sender=ClassAttendingDetail)
def manage_time(sender, instance, *args, **kwargs):
    if instance.from_time and not instance.to_time:
        from_time = instance.routine_detail.from_time
        to_time = instance.routine_detail.to_time
        time_diff = datetime.combine(date.today(), to_time) - datetime.combine(date.today(), from_time)
        new_to_time = (datetime.combine(datetime.now().date(), instance.from_time) + timedelta(
            seconds=time_diff.seconds)).time()
        instance.to_time = new_to_time


@receiver(post_save, sender=ClassAttendingDetail)
def send_notification(sender, instance, created, *args, **kwargs):
    year = instance.routine_detail.routine_of.year
    part = instance.routine_detail.routine_of.part
    programme = instance.routine_detail.routine_of.programme
    group = instance.routine_detail.routine_of.group
    remark = instance.remark
    if True:
        if not instance.is_attending:
            text = 'Teacher cannot attend class %s @ %s on %s, remark: %s' % (
                instance.routine_detail.subject, instance.routine_detail.from_time.strftime("%H:%M:%S %p"),
                str(instance.date), remark)
        else:
            text = 'Time of %s on %s changed from %s to %s. Remark: %s' % (
                instance.routine_detail.subject, instance.date,
                instance.routine_detail.from_time.strftime("%H:%M:%S %p"),
                instance.from_time.strftime("%H:%M:%S %p"), remark)
        crs = StudentDetail.objects.filter(is_class_representative=True)
        cr_phone = [stu.phone for stu in crs if (stu.current_year == year and stu.current_part == part)]
        phone_number = ', '.join(cr_phone)
        _thread.start_new_thread(send_sms, (phone_number, text, instance.teacher.teacher_detail.short_name))

    if instance.notify:
        context = {
            'instance': instance
        }

        filtered_emails = [stu.email for stu in StudentDetail.objects.all() if
                           (stu.current_year == year and stu.current_part == part and stu.programme == programme
                            and stu.group == group)]
        if instance.is_cancelled:
            subject = 'Class cancelled'
            template = 'routine/class_cancelled.html'
        elif not instance.is_attending:
            subject = 'Teacher not attending class'
            template = 'routine/class_not_attending.html'
        else:
            subject = 'Routine updated'
            template = 'routine/class_updated.html'
        _thread.start_new_thread(send_email, (subject, template, context, filtered_emails))
