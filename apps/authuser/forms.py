import io

from django import forms

from apps.authuser.models import Department
from apps.constants import *
from apps.information.models import Programme

REQUIRED_FIELDS_FOR_STUDENTS = [NAME_FIELD, EMAIL_FIELD, PHONE_FIELD, GROUP_FIELD, ROLL_NUMBER_FIELD]
REQUIRED_FIELDS_FOR_TEACHERS = [NAME_FIELD, EMAIL_FIELD, PHONE_FIELD]


def validate_file_for_students(value):
    if not value.name.endswith('.csv'):
        raise forms.ValidationError("Only CSV file is accepted")
    import csv
    decoded_file = value.read().decode('utf-8')
    io_string = io.StringIO(decoded_file)
    reader = csv.reader(io_string, delimiter=',', quotechar='|')
    row = next(reader)
    for field in REQUIRED_FIELDS_FOR_STUDENTS:
        if field not in row:
            raise forms.ValidationError(
                " \'%s\' field is not present in the uploaded file. Required fields are %s " % (
                    field, ', '.join(REQUIRED_FIELDS_FOR_STUDENTS)))
    value.seek(0)


def validate_file_for_teachers(value):
    if not value.name.endswith('.csv'):
        raise forms.ValidationError("Only CSV file is accepted")
    import csv
    decoded_file = value.read().decode('utf-8')
    io_string = io.StringIO(decoded_file)
    reader = csv.reader(io_string, delimiter=',', quotechar='|')
    row = next(reader)
    for field in REQUIRED_FIELDS_FOR_TEACHERS:
        if field not in row:
            raise forms.ValidationError(
                " \'%s\' field is not present in the uploaded file. Required fields are %s " % (
                    field, ', '.join(REQUIRED_FIELDS_FOR_TEACHERS)))
    value.seek(0)


class DetailsForUploadingStudentCSVForm(forms.Form):
    batch = forms.ChoiceField(choices=BATCH_CHOICES)
    programme = forms.ModelChoiceField(queryset=Programme.objects.all(), )
    csv_file = forms.FileField(validators=[validate_file_for_students],
                               help_text='Required fields are %s' % (', '.join(REQUIRED_FIELDS_FOR_STUDENTS, )))


class DetailsForUploadingTeacherCSVForm(forms.Form):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), )
    csv_file = forms.FileField(validators=[validate_file_for_teachers],
                               help_text='Required fields are %s' % (', '.join(REQUIRED_FIELDS_FOR_TEACHERS, )))
