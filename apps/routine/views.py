from datetime import datetime

from django.utils.dateparse import parse_date
# Create your views here.
from rest_framework.generics import ListAPIView

from apps.routine.models import RoutineDetail, Routine
from apps.routine.serializers import RoutineDetailSerializer


class GetRoutineView(ListAPIView):
    serializer_class = RoutineDetailSerializer
    queryset = RoutineDetail.objects.all()

    def get_queryset(self):
        date_str = self.request.GET.get('date', str(datetime.now().date()))
        date = parse_date(date_str)
        week_day = date.weekday()
        week_day = (week_day+1) % 7
        if self.request.user.is_student and hasattr(self.request.user, 'student_detail'):
            current_year = self.request.user.student_detail.current_year
            current_part = self.request.user.student_detail.current_part
            programme = self.request.user.student_detail.programme
            group = self.request.user.student_detail.group
            routine_instance = Routine.objects.filter(year=current_year, part=current_part, programme=programme,
                                                      group=group)
            routine_details = RoutineDetail.objects.filter(routine_of__in=routine_instance, day_of_week=week_day)
            return routine_details
        elif self.request.user.is_teacher and hasattr(self.request.user, 'teacher_detail'):
            routine_details = RoutineDetail.objects.filter(teachers=self.request.user)

            return routine_details
        return self.queryset.none()
