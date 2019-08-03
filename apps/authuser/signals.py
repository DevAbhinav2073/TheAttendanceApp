import _thread
from random import randint

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.authtoken.models import Token

from apps.authuser.models import StudentDetail, TeacherDetail
from apps.constants import USER_TYPE_STUDENT, USER_TYPE_TEACHER

User = get_user_model()


def send_account_creation_email(detail):
    return
    context = {
        'detail': detail
    }
    from_email = 'classinfo@no-reply.com'
    subject = 'Account created at Classroom Updates'
    html_content = render_to_string(template_name='admin/authuser/account_creation_email.html',
                                    context=context)  # render with dynamic value
    text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.

    # create the email, and attach the HTML version as well.
    msg = EmailMultiAlternatives(subject, text_content, from_email, [detail.email, ])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def get_random_password():
    pw = randint(100000, 999999)
    return str(pw)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance, created, *args, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=StudentDetail)
def create_student_user(sender, instance, created, *args, **kwargs):
    if created and not instance.user:
        user = User.objects.create(username=instance.email)
        user.email = instance.email
        password = get_random_password()
        instance.password = password
        user.set_password(password)
        user.user_type = USER_TYPE_STUDENT
        instance.user = user
        instance.save()
        user.save()
        _thread.start_new_thread(send_account_creation_email, (instance,))
    else:
        user = instance.user
        user.email = instance.email
        user.username = instance.email
        user.save()


@receiver(post_save, sender=TeacherDetail)
def create_teacher_user(sender, instance, created, *args, **kwargs):
    if created and not instance.user:
        user = User.objects.create(username=instance.email)
        user.email = instance.email
        password = get_random_password()
        instance.password = password
        user.set_password(password)
        user.user_type = USER_TYPE_TEACHER
        instance.user = user
        instance.save()
        user.save()
        _thread.start_new_thread(send_account_creation_email, (instance,))
    else:
        user = instance.user
        user.email = instance.email
        user.username = instance.email
        user.save()
