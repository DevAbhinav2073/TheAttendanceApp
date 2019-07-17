from django.db import models

from apps.constants import *


class Routine(models.Model):
    programme = models.ForeignKey('information.Programme', on_delete=models.PROTECT)
    year = models.CharField(max_length=5, choices=YEAR_CHOICES)
    part = models.CharField(max_length=5, choices=PART_CHOICES)
    group = models.CharField(max_length=1, choices=GROUP_CHOICES)

    def __str__(self):
        return 'Routine instance of %s, year: %s    , part: %s, group %s' % (
            self.programme, self.year, self.part, self.group)


class RoutineDetail(models.Model):
    routine_of = models.ForeignKey('routine.Routine', on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DAY_OF_WEEK_CHOICES_TUPLE)
    teachers = models.ManyToManyField('authuser.Teacher', limit_choices_to={
        'user_type': USER_TYPE_TEACHER
    }, blank=True)
    from_time = models.TimeField(default=datetime.now)
    to_time = models.TimeField(default=datetime.now)
    subject = models.CharField(max_length=100, blank=True, null=True,
                               help_text='Can be anything like break presentation etc, not necesserily a subject from syllabus')
    room = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return 'Routine of day %s of week from %s to %s' % (
            self.day_of_week, str(self.from_time), str(self.to_time))

    def has_corrected_detail(self, date):
        queryset = ClassAttendingDetail.objects.filter(date=date, routine_detail=self)
        has_corrected_detail = queryset.exists()
        self.corrected_info = queryset.first()
        return has_corrected_detail

    def corrected_from_time(self, date):
        if self.has_corrected_detail(date):
            return self.corrected_info.from_time
        return self.from_time

    def corrected_to_time(self, date):
        if self.has_corrected_detail(date):
            return self.corrected_info.to_time
        return self.to_time

    def is_cancelled(self, date):
        if self.has_corrected_detail(date):
            return self.corrected_info.is_cancelled
        return False

    def is_attending(self, date):
        if self.has_corrected_detail(date):
            return self.corrected_info.is_attending
        return True

    @property
    def teachers_name(self):
        teacher_name_list = []
        for teacher in self.teachers.all():
            if hasattr(teacher, 'teacher_detail'):
                teacher_name_list.append(teacher.teacher_detail.name)
        return ', '.join(teacher_name_list)

    class Meta:
        ordering = ('from_time', 'to_time',)


class ClassAttendingDetail(models.Model):
    routine_detail = models.ForeignKey('routine.RoutineDetail', related_name='corrected_detail',
                                       on_delete=models.CASCADE)
    teacher = models.ForeignKey('authuser.Teacher', on_delete=models.CASCADE)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_update = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=150, null=True, blank=True)
    send_sms = models.BooleanField(default=False)
    date = models.DateField()
    from_time = models.TimeField(null=True, blank=True)
    to_time = models.TimeField(null=True, blank=True)
    is_attending = models.BooleanField(default=True)  # to know if the teacher is attending or not
    is_permanent = models.BooleanField(default=False)  # to change the default routine
    is_cancelled = models.BooleanField(default=False)  # to cancel a class
    notify = models.BooleanField(default=True)
    allow_csv_upload = True

    def __str__(self):
        return 'Attending detail of %s' % (self.routine_detail,)


class SMSCredit(models.Model):
    credit_count = models.IntegerField(default=5)

    @staticmethod
    def has_credit():
        try:
            return SMSCredit.objects.all().first().credit_count > 0
        except:
            return False

    @staticmethod
    def deduct_credit(num: int):
        try:
            instance = SMSCredit.objects.all().first()
            instance.credit_count = instance.credit_count - num
            instance.save()
        except:
            pass

    @staticmethod
    def add_credit(num: int):
        try:
            instance = SMSCredit.objects.all().first()
            instance.credit_count = instance.credit_count + num
            instance.save()
        except:
            pass

    @staticmethod
    def credit_count(num: int):
        try:
            instance = SMSCredit.objects.all().first()
            return instance.credit_count
        except:
            pass

    def __str__(self):
        return str(self.credit_count)
