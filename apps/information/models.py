from django.conf import settings
from django.db import models

# Create your models here.
from apps.constants import YEAR_CHOICES, PART_CHOICES, BATCH_CHOICES


class Department(models.Model):
    name = models.CharField(max_length=50, )

    def __str__(self):
        return self.name


class Programme(models.Model):
    name = models.CharField(max_length=50)
    short_form = models.CharField(max_length=5,
                                  help_text='This is the abbreviated form that is used in roll number. For example BCT for Computer Engineering')
    department = models.ForeignKey(settings.DEPARTMENT_MODEL, related_name='programmes', on_delete=models.SET_NULL,
                                   null=True)
    groups = models.CharField(max_length=50, help_text='Enter groups separated by commas', default='A, B')

    @property
    def groups_list(self):
        return [group.strip() for group in self.groups.split(',')]

    def __str__(self):
        return self.name


class Notice(models.Model):
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    batch = models.CharField(max_length=5, choices=BATCH_CHOICES, null=True, blank=True)
    year = models.CharField(max_length=4, choices=YEAR_CHOICES)
    part = models.CharField(max_length=4, choices=PART_CHOICES)
    message = models.CharField(max_length=140)
    send_sms = models.BooleanField(default=False)
    send_email = models.BooleanField(default=True)
    notice_by = models.ForeignKey('authuser.Teacher', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('-id',)
