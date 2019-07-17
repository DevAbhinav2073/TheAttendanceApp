import io

from django import forms

from .utils import get_required_fields


def validate_file_for_fields(required_fields):
    def validate_file_for_fields_inner(value):
        if not value.name.endswith('.csv'):
            raise forms.ValidationError("Only CSV file is accepted")
        import csv
        decoded_file = value.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string, delimiter=',', quotechar='|')
        row = next(reader)
        for field in required_fields:
            if field not in row:
                raise forms.ValidationError(
                    " \'%s\' field is not present in the uploaded file. Required field(s) is/are: %s " % (
                        field, ', '.join(required_fields)))
        value.seek(0)

    return validate_file_for_fields_inner


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model')
        super().__init__(*args, **kwargs)
        required_fields = get_required_fields(self.model)
        self.fields['csv_file'].help_text = 'Required field(s) is/are: %s' % (', '.join(required_fields, ))
        self.fields['csv_file'].validators = [validate_file_for_fields(required_fields), ]
