from datetime import datetime

from django.conf import settings
from django.db import models
# Create your models here.
from django.urls import reverse

THEORY_PRACTICAL_CHOICES = (
    ('th', 'Theory'),
    ('pr', 'Practical'),
)

YEAR_CHOICES = (
    ("I", "I"),
    ("II", "II"),
    ("III", "III"),
    ('IV', "IV"),
    ('V', "V"),
)
PART_CHOICES = (
    ('I', "I"),
    ('II', "II"),
)
YEAR_UP_TO = 2076
BATCH_CHOICES_TUPLE = [(str(year), str(year)) for year in range(2070, YEAR_UP_TO)]


#
# class Department(models.Model):
#     name = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.name
#
#
# class Programme(models.Model):
#     name = models.CharField(max_length=60)
#     short_form = models.CharField(max_length=10, unique=True, help_text='For example BCT for BE Computer')
#     department = models.ForeignKey(settings.DEPARTMENT_MODEL, related_name='programmes', on_delete=models.SET_NULL,
#                                    null=True)
#     groups = models.CharField(max_length=50, help_text='Enter groups separated by commas', default='A, B')
#
#     @property
#     def groups_list(self):
#         return self.groups.split(',')
#
#     def __str__(self):
#         return self.name
#
#
# class Student(models.Model):
#     name = models.CharField(max_length=100)
#     programme = models.ForeignKey(Programme, null=True, on_delete=models.SET_NULL)
#     roll_number = models.CharField(max_length=10)
#     batch = models.CharField(max_length=4, choices=BATCH_CHOICES_TUPLE)
#     group = models.CharField(max_length=1)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         unique_together = ('programme', 'batch', 'roll_number')

class SubjectDetail(models.Model):
    name = models.CharField(max_length=60)
    subject_code = models.CharField(max_length=20, unique=True)
    theory_full_marks = models.IntegerField(default=0, help_text="Full marks of theory")
    practical_full_marks = models.IntegerField(default=0, help_text="Full marks of theory")

    def __str__(self):
        return self.name


class CourseDetail(models.Model):
    subject = models.ForeignKey(SubjectDetail, on_delete=models.CASCADE)
    programme = models.ForeignKey(settings.PROGRAMME_MODEL, related_name='course_detail', on_delete=models.PROTECT)
    year = models.CharField(max_length=4, choices=YEAR_CHOICES)
    part = models.CharField(max_length=4, choices=PART_CHOICES)

    def has_marks(self, batch, th_pr, group):
        return MarksInstance.objects.filter(batch=batch, year=self.year, part=self.part, programme=self.programme,
                                            subject=self.subject, theory_practical=th_pr, group=group).exists()

    def get_marks_detail(self, batch, th_pr, group):
        if self.has_marks(batch, th_pr, group):
            return MarksInstance.objects.filter(batch=batch, year=self.year, part=self.part, programme=self.programme,
                                                subject=self.subject, theory_practical=th_pr, group=group).first()

    def get_marks_seeing_url(self, batch, th_pr, group):
        if self.has_marks(batch, th_pr, group):
            url = reverse('display_result_ac_instance',
                          kwargs={'marks_instance_id': self.get_marks_detail(batch, th_pr, group).id})
            return url

    def __str__(self):
        return self.subject.name


class MarksInstance(models.Model):
    batch = models.CharField(max_length=4, choices=BATCH_CHOICES_TUPLE)
    year = models.CharField(max_length=3, choices=YEAR_CHOICES)
    part = models.CharField(max_length=3, choices=PART_CHOICES)
    subject = models.ForeignKey(SubjectDetail, on_delete=models.PROTECT)
    theory_practical = models.CharField(max_length=30, choices=THEORY_PRACTICAL_CHOICES)
    group = models.CharField(max_length=1)
    programme = models.ForeignKey(settings.PROGRAMME_MODEL, on_delete=models.SET_NULL, null=True)
    date = models.DateField(default=datetime.now, null=True)
    name_of_examiner = models.CharField(max_length=60, null=True)
    pass_mark = models.IntegerField(null=True)
    full_mark = models.IntegerField(null=True)

    def __str__(self):
        return 'Mark sheet of batch %s, (Year: %s, Part: %s) group: %s' % (self.batch, self.year, self.part, self.group)

    class Meta:
        ordering = ('-id',)
        permissions = (
            ("can_enter_result", "Can take test"),
        )


class MarksDetail(models.Model):
    marks_instance = models.ForeignKey(MarksInstance, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.STUDENT_MODEL, on_delete=models.PROTECT)
    marks = models.CharField(max_length=4)

    def __str__(self):
        return 'Marks of %s' % (self.marks_instance,)
