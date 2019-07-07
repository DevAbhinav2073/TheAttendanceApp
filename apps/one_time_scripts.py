from apps.authuser.models import TeacherDetail, StudentDetail
from apps.constants import *


def manage_email():
    try:
        for detail in TeacherDetail.objects.all():
            user = detail.user
            user.email = detail.email
            user.username = detail.email
            user.user_type = USER_TYPE_TEACHER
            user.save()
        for detail in StudentDetail.objects.all():
            user = detail.user
            user.email = detail.email
            user.user_type = USER_TYPE_STUDENT
            user.username = detail.email
            user.save()
    except Exception as e:
        print(e)
