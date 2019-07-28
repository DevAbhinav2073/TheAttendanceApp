from datetime import datetime

from rest_framework.generics import get_object_or_404

from apps.routine.models import SemesterDetail


def get_current_semester(year=None, part=None):
    if year and part:
        semester_detail = get_object_or_404(SemesterDetail.objects.all(), year=year, part=part)
        return semester_detail
    else:
        date = datetime.now().date()
        semester_detail = SemesterDetail.objects.filter(from_date__lte=date, to_date__gte=date).first()
    if semester_detail:
        return semester_detail
    return SemesterDetail.objects.all().first()  # since ordering is in reverse order
