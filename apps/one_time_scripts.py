from apps.authuser.models import TeacherDetail, StudentDetail


def manage_email():
    try:
        for detail in TeacherDetail.objects.all():
            user = detail.user
            user.email = detail.email
            user.username = detail.email
            user.save()
        for detail in StudentDetail.objects.all():
            user = detail.user
            user.email = detail.email
            user.username = detail.email
            user.save()
    except:
        pass
