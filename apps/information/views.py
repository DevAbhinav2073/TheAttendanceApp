# Create your views here.
from rest_framework.viewsets import ModelViewSet

from apps.information.models import Notice, Department, Programme
from apps.information.serializers import NoticeSerializer, DepartmentSerializer, ProgrammeSerializer


class NoticeViewSet(ModelViewSet):
    serializer_class = NoticeSerializer
    queryset = Notice.objects.all()

    def get_queryset(self):
        if self.request.user.is_teacher:
            return self.queryset.filter(notice_by=self.request.user)
        else:
            return self.queryset.filter(batch=self.request.user.student_detail.batch,
                                        year=self.request.user.student_detail.current_year,
                                        part=self.request.user.student_detail.current_part
                                        )
        return self.queryset


class DepartmentViewSet(ModelViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()


class ProgrammeViewSet(ModelViewSet):
    serializer_class = ProgrammeSerializer
    queryset = Programme.objects.all()
