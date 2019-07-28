from datetime import datetime

from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_date
# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.routine.models import RoutineDetail, Routine, ClassAttendingDetail, ArrivalTime
from apps.routine.serializers import RoutineDetailSerializer, ClassAttendingSerializer, ArrivalTimeSerializer
from apps.routine.utils import get_current_semester


def get_corrected_queryset(queryset, date):
    for obj in queryset:
        extra_details = ClassAttendingDetail.objects.filter(routine_detail=obj, date=date)
        if extra_details.exists():
            extra_detail = extra_details.first()
            obj.from_time = extra_detail.from_time
            obj.to_time = extra_detail.to_time


class GetRoutineView(ListAPIView):
    serializer_class = RoutineDetailSerializer
    queryset = RoutineDetail.objects.all()

    def get_serializer_context(self):
        return {
            'date': self.date
        }

    def get_queryset(self):
        date_str = self.request.GET.get('date', str(
            datetime.now().date()))  # converting date to string, so that both the values are of same datatype
        is_corrected = self.request.GET.get('corrected', '0')
        try:
            is_corrected = int(is_corrected)
            is_corrected = bool(is_corrected)
        except:
            pass
        # converting string to date object
        date = parse_date(date_str)
        week_day = date.weekday()
        self.date = date
        self.is_corrected = is_corrected
        # For international calender, first day of week is Monday, but for nepal it is Sunday
        week_day = (week_day + 1) % 7
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
            routine_details = RoutineDetail.objects.filter(teachers=self.request.user, day_of_week=week_day)

            return routine_details
        return self.queryset.none()


class ClassAttendingViewSet(ModelViewSet):
    serializer_class = ClassAttendingSerializer
    queryset = ClassAttendingDetail.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['teacher'] = str(request.user.id)
        serialized = ClassAttendingSerializer(data=data)
        if serialized.is_valid(raise_exception=True):
            date = serialized.validated_data.get('date')
            routine_of = serialized.validated_data.get('routine_detail')
            ClassAttendingDetail.objects.filter(date=date, routine_detail=routine_of).delete()
            instance = serialized.save()
            headers = self.get_success_headers(serialized.data)
            return Response(serialized.data, status=status.HTTP_201_CREATED, headers=headers)


class ArrivalTimeViewSet(ModelViewSet):
    serializer_class = ArrivalTimeSerializer
    queryset = ArrivalTime.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        serialized = ArrivalTimeSerializer(data=data)
        if serialized.is_valid(raise_exception=True):
            date = serialized.validated_data.get('date')
            routine_of = serialized.validated_data.get('routine_detail')
            ArrivalTime.objects.filter(date=date, routine_detail=routine_of).delete()
            instance = serialized.save()
            headers = self.get_success_headers(serialized.data)
            return Response(serialized.data, status=status.HTTP_201_CREATED, headers=headers)


User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def get_stats(request, teacher_id):
    teacher = get_object_or_404(User.objects.all(), id=teacher_id)
    year = request.GET.get('year', None)
    part = request.GET.get('part', None)
    current_semester = get_current_semester(year, part)
    routine_alter_detail_of_this_teacher = ClassAttendingDetail.objects.filter(teacher=teacher,
                                                                               date__lte=current_semester.to_date,
                                                                               date__gte=current_semester.from_date)
    arrival_time_detail_of_this_teacher = ArrivalTime.objects.filter(routine_detail__teachers=teacher,
                                                                     date__lte=current_semester.to_date,
                                                                     date__gte=current_semester.from_date)
    cancelled_count = routine_alter_detail_of_this_teacher.filter(is_cancelled=True).count()
    not_attended_count = routine_alter_detail_of_this_teacher.filter(is_attending=False).count()
    arrived_late_count = arrival_time_detail_of_this_teacher.count()
    return Response({
        'cancelled': cancelled_count,
        'not_attended': not_attended_count,
        'arrived_late': arrived_late_count
    })
