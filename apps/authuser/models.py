from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

# Create your models here.
from apps.constants import *


class User(AbstractUser):
    user_type = models.CharField(max_length=10, choices=(
        (USER_TYPE_STUDENT, USER_TYPE_STUDENT),
        (USER_TYPE_TEACHER, USER_TYPE_TEACHER)
    ), default=USER_TYPE_TEACHER)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def is_student(self):
        return self.user_type == USER_TYPE_STUDENT

    @property
    def is_teacher(self):
        return self.user_type == USER_TYPE_TEACHER


class StudentManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type=USER_TYPE_STUDENT)


class Student(User):
    objects = StudentManager

    class Meta:
        proxy = True


class TeacherManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type=USER_TYPE_TEACHER)


class Teacher(User):
    objects = TeacherManager

    class Meta:
        proxy = True


class TeacherDetail(models.Model):
    user = models.OneToOneField('authuser.User', limit_choices_to={
        'user_type': USER_TYPE_TEACHER
    }, related_name='teacher_detail', on_delete=models.CASCADE)
    is_full_timer = models.BooleanField(default=True)
    subjects = models.CharField(max_length=100, null=True)
    def __str__(self):
        return 'Details of %s teacher' % (self.user.get_full_name(),)


class StudentDetail(models.Model):
    user = models.OneToOneField('authuser.User', limit_choices_to={
        'user_type': USER_TYPE_STUDENT
    }, related_name='student_detail', on_delete=models.CASCADE)
    batch = models.CharField(max_length=10, choices=BATCH_CHOICES)
    programme = models.ForeignKey('information.Programme', on_delete=models.CASCADE)
    roll_number = models.IntegerField()
    current_year = models.CharField(max_length=5, choices=YEAR_CHOICES)
    current_part = models.CharField(max_length=5, choices=PART_CHOICES)
    group = models.CharField(max_length=1, choices=GROUP_CHOICES)

    def __str__(self):
        return 'Details of %s student' % (self.user.get_full_name(),)
