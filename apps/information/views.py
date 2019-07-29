# Create your views here.
from rest_framework.viewsets import ModelViewSet

from apps.information.models import Notice
from apps.information.serializers import NoticeSerializer


class NoticeViewSet(ModelViewSet):
    serializer_class = NoticeSerializer
    queryset = Notice.objects.all()
