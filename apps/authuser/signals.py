from random import randint

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from apps.authuser.models import StudentDetail, TeacherDetail

User = get_user_model()


def get_random_password():
    pw = randint(100000, 999999)
    return str(pw)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance, created, *args, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=StudentDetail)
def create_student_user(sender, instance, created, *args, **kwargs):
    if created:
        user = User.objects.create(username=instance.email)
        user.email = instance.email
        password = get_random_password()
        instance.password = password
        user.set_password(password)
        instance.user = user
        instance.save()
        user.save()


@receiver(post_save, sender=TeacherDetail)
def create_teacher_user(sender, instance, created, *args, **kwargs):
    if created:
        user = User.objects.create(username=instance.email)
        user.email = instance.email
        password = get_random_password()
        instance.password = password
        user.set_password(password)
        instance.user = user
        instance.save()
        user.save()
