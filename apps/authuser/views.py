from datetime import datetime

import timestring
from django.contrib.auth import get_user_model
# Create your views here.
from rest_framework import parsers, renderers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.authuser.models import Feedback
from apps.authuser.serializers import UserSerializer, convert_to_english, FeedbackSerializer
from apps.constants import USER_TYPE_TEACHER, USER_TYPE_STUDENT

User = get_user_model()


def is_end_of_semester(date=datetime.now().date()):
    nep_date_string = '%d-%d-%d' % (2070, 7, 1)  # kartik 1 start of semester
    en_date_object = convert_to_english(nep_date_string)
    # days_difference = en_date_object_now - en_date_object
    days_difference = date - en_date_object
    days_spent_in_semester = days_difference.days % 180
    if (int(days_difference.days / 180) + 1) % 2 == 0:
        if days_spent_in_semester > 115:
            return True
    else:
        if days_spent_in_semester > 140:
            return True
    return False


class LoginAPIView(APIView):
    throttle_classes = ()
    permission_classes = ()
    queryset = User.objects.all()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        serialized_profile = UserSerializer(user)
        return Response(serialized_profile.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_own_detail(request):
    return Response(UserSerializer(request.user).data)


@api_view(['GET'])
def can_send_feedback(request):
    date = request.GET.get('date', str(datetime.now().date()))
    date = timestring.Date(date).date.date()
    return Response({
        'can_give_feedback': is_end_of_semester(date),
    })


class FeedbackViewSet(ModelViewSet):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()

    def get_queryset(self):
        if self.request.user.user_type == USER_TYPE_TEACHER:
            return self.queryset.filter(teacher=self.request.user)
        elif self.request.user.user_type == USER_TYPE_STUDENT:
            return self.queryset.filter(feedback_by=self.request.user)
        else:
            return self.queryset.none()

    def create(self, request, *args, **kwargs):
        date = request.GET.get('date', str(datetime.now().date()))
        date = timestring.Date(date).date.date()
        if is_end_of_semester(date):
            return Response({
                'detail': 'Cannot accept feedback now'
            })
        return super().create(request, *args, **kwargs)