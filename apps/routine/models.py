from datetime import datetime

from django.db import models

from apps.constants import *


class Routine(models.Model):
    programme = models.ForeignKey('information.Programme', on_delete=models.PROTECT)
    year = models.IntegerField(choices=(
        (1, 'I'),
        (2, 'II'),
        (3, 'III'),
        (4, 'IV'),
        (5, 'V'),
    ))
    part = models.IntegerField(choices=(
        (1, 'I'),
        (2, 'II'),
    ))
    group = models.CharField(max_length=1, choices=GROUP_CHOICES)


class RoutineDetail(models.Model):
    day_of_week = models.IntegerField(choices=DAY_OF_WEEK_CHOICES_TUPLE)
    teacher = models.ForeignKey('authuser.Teacher', on_delete=models.SET_NULL, null=True, blank=True)
    from_time = models.TimeField(default=datetime.now)
    to_time = models.TimeField(default=datetime.now)
    subject = models.CharField(max_length=100, blank=True, null=True,
                               help_text='Can be anything like break presentation etc, not necesserily a subject from syllabus')

    def __str__(self):
        return 'Routine of day %s of week of teacher %s from %s to %s' % (
            self.day_of_week, self.teacher, str(self.from_time), str(self.to_time))


