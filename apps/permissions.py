from rest_framework.permissions import BasePermission

from apps.constants import USER_TYPE_TEACHER, USER_TYPE_STUDENT


class IsTeacher(BasePermission):
    """
    Allows access only to Teacher users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.user_type == USER_TYPE_TEACHER)


class IsStudent(BasePermission):
    """
    Allows access only to STUDENT users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.user_type == USER_TYPE_STUDENT)


class IsCR(BasePermission):
    """
    Allows access only to CR users.
    """

    def has_permission(self, request, view):
        if bool(
                request.user and request.user.is_authenticated and request.user.user_type == USER_TYPE_STUDENT and hasattr(
                    request.user, 'student_detail')):
            return request.user.student_detail.is_class_representataive
        return False


def is_teacher(user):
    return bool(user and user.is_authenticated and user.user_type == USER_TYPE_TEACHER)


def is_student(user):
    return bool(user and user.is_authenticated and user.user_type == USER_TYPE_STUDENT)


def is_cr(user):
    if bool(
            user and user.is_authenticated and user.user_type == USER_TYPE_STUDENT and hasattr(
                user, 'student_detail')):
        return user.student_detail.is_class_representataive
    return False
