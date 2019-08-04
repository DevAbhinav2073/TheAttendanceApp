"""TheAttendanceApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter

from apps.authuser.views import LoginAPIView, get_own_detail, can_send_feedback, FeedbackViewSet, get_list_of_teachers, \
    upload_image
from apps.im.views import get_internal_marks
from apps.information.views import *
from apps.routine.views import GetRoutineView, ClassAttendingViewSet, get_stats, ArrivalTimeViewSet

router = DefaultRouter()
router.register('class-attending-detail', ClassAttendingViewSet)
router.register('arrival-time-detail', ArrivalTimeViewSet)
router.register('feedback', FeedbackViewSet)
router.register('notice', NoticeViewSet)
router.register('department', DepartmentViewSet)
router.register('programme', ProgrammeViewSet)

urlpatterns = [
                  path('', RedirectView.as_view(url='im/')),
                  path('admin/', admin.site.urls),
                  path('api/login/', LoginAPIView.as_view(), name='login'),
                  path('api/get_own_detail/', get_own_detail, name='get_own_detail'),
                  path('api/get_routine/', GetRoutineView.as_view(), name='get_routine'),
                  path('api/can_send_feedback/', can_send_feedback, name='can_send_feedback'),
                  path('api-auth/', include('rest_framework.urls')),
                  path('api/rest-auth/', include('rest_auth.urls')),
                  path('api/', include(router.urls)),
                  path('api/get_stats/<int:teacher_id>/', get_stats, name='get_stats_ac_teacher'),
                  path('api/get_list_of_teachers/', get_list_of_teachers, name='get_list_of_teachers'),
                  path('api/upload_image/', upload_image, name='upload_image'),
                  path('api/get_internal_marks/', get_internal_marks, name='get_internal_marks'),
                  path('csv_uploader/', include('apps.csv_uploader.urls')),
                  path('im/', include('apps.im.urls')),

              ] \
              + static('static', document_root=settings.STATIC_ROOT) \
              + static('media', document_root=settings.MEDIA_ROOT)
