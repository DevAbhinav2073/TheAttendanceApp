from django import forms
from django.apps import apps

from .models import *

Student = apps.get_model(settings.STUDENT_MODEL)
Programme = apps.get_model(settings.PROGRAMME_MODEL)
Department = apps.get_model(settings.DEPARTMENT_MODEL)


class YearPartFrom(forms.Form):
    batch = forms.ChoiceField(choices=BATCH_CHOICES_TUPLE)
    year = forms.ChoiceField(choices=YEAR_CHOICES)
    part = forms.ChoiceField(choices=PART_CHOICES)


class SeeMarksForm(forms.Form):
    batch = forms.ChoiceField(choices=BATCH_CHOICES_TUPLE)
    year = forms.ChoiceField(choices=YEAR_CHOICES)
    part = forms.ChoiceField(choices=PART_CHOICES)
    subject = forms.ModelChoiceField(queryset=SubjectDetail.objects.all())
    theory_practical = forms.ChoiceField(choices=THEORY_PRACTICAL_CHOICES)
    group = forms.CharField()
    programme = forms.ModelChoiceField(queryset=Programme.objects.all())
