from datetime import datetime

from rest_framework.generics import get_object_or_404

from apps.routine.models import SemesterDetail


def get_integer_value(value):
    if isinstance(value, int):
        return value
    if value in ['i', 'I']:
        return 1
    elif value in ['ii', 'II']:
        return 2
    elif value in ['iii', 'III']:
        return 3
    elif value in ['iv', 'IV']:
        return 4
    elif value in ['v', 'V']:
        return 5
    return 1


def get_roman_value(value):
    value = int(value)
    if value == 1:
        return 'I'
    elif value == 2:
        return 'II'
    elif value == 3:
        return 'III'
    elif value == 4:
        return 'IV'
    elif value == 5:
        return 'V'
    return value


def get_current_semester(year=None, part=None):
    if year and part:
        semester_detail = get_object_or_404(SemesterDetail.objects.all(), academic_year=year, part=part)
        return semester_detail
    else:
        date = datetime.now().date()
        semester_detail = SemesterDetail.objects.filter(from_date__lte=date, to_date__gte=date).first()
    if semester_detail:
        return semester_detail
    return SemesterDetail.objects.all().first()  # since ordering is in reverse order


def get_batch(year='i', part='i'):
    year = get_integer_value(year)
    part = get_integer_value(part)
    from_days = ((year - 1) * 365) + (180 * (part - 1))
    to_days = ((year - 1) * 365) + (180 * part)

    for semester_detail in SemesterDetail.objects.all():
        time_difference = datetime.now().date() - semester_detail.from_date
        if time_difference.days in range(from_days, to_days):
            return semester_detail.academic_year
    return SemesterDetail.objects.all().first().academic_year
