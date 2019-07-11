from apps.authuser.models import TeacherDetail, StudentDetail
from apps.authuser.signals import get_random_password
from apps.constants import *


def manage_email():
    try:
        for detail in TeacherDetail.objects.all():
            user = detail.user
            user.email = detail.email
            user.username = detail.email
            user.user_type = USER_TYPE_TEACHER
            password = get_random_password()
            user.set_password(password)
            detail.password = password
            user.save()
            detail.save()
            print(user.username, password)
        for detail in StudentDetail.objects.all():
            user = detail.user
            user.email = detail.email
            user.user_type = USER_TYPE_STUDENT
            user.username = detail.email
            password = get_random_password()
            user.set_password(password)
            detail.password = password
            user.save()
            detail.save()
            print(user.username, password)
    except Exception as e:
        print(e)
