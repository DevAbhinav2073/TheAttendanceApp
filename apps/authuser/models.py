from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from apps.constants import *
from apps.date_converter import convert_to_english


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
    }, null=True, related_name='teacher_detail', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='')
    email = models.EmailField()
    phone = models.CharField(max_length=14, blank=True, null=True)
    is_full_timer = models.BooleanField(default=True)
    subjects = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class StudentDetail(models.Model):
    user = models.OneToOneField('authuser.User', limit_choices_to={
        'user_type': USER_TYPE_STUDENT
    },
                                related_name='student_detail',
                                null=True,
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=14, blank=True, null=True)
    batch = models.CharField(max_length=10, choices=BATCH_CHOICES)
    programme = models.ForeignKey('information.Programme', on_delete=models.CASCADE)
    roll_number = models.IntegerField()
    group = models.CharField(max_length=1, choices=GROUP_CHOICES)
    is_class_representative = models.BooleanField(default=False)
    password = models.CharField(max_length=50, blank=True, null=True)

    def clean(self):
        super().clean()
        if self.is_class_representative and not self.phone:
            raise ValidationError({'phone': 'A CR must have a phone number'})

    @property
    def date_difference(self):
        nep_date_string = '%s-%d-%d' % (self.batch, 7, 1)
        en_date_object = convert_to_english(nep_date_string)
        days_difference = datetime.now().date() - en_date_object
        return days_difference.days

    @property
    def current_year(self):
        year = ['I', 'II', 'III', 'IV', 'V']
        for i in range(1, 6):
            if self.date_difference in range(0, 365 * i):
                return year[i - 1]
        return 'None'

    @property
    def current_part(self):
        year = ['I', 'II']
        for i in range(1, 3):
            if self.date_difference % 365 in range(0, 180 * i):
                return year[i - 1]
        return 'None'

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.current_year_cal)