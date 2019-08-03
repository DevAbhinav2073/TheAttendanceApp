"""InternalMarks URL Configuration

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
from django.urls import path, include

from apps.im.views import *

urlpatterns = [
    path('', index, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('enter_marks', enter_marks, name='enter_marks'),
    path('see_marks', see_marks, name='see_marks'),
    path('dept_see_records', dept_see_records, name='see_records_department'),
    path('stu_see_records', stu_see_records, name='see_records_student'),
    path('csv_uploader/', include('apps.csv_uploader.urls')),
    path('api/get_subjects', get_subjects),
    path('api/get_students', get_students),
    path('display_result', display_result, name='display_result'),
    path('display/<int:marks_instance_id>/', display_result_ac_instance, name='display_result_ac_instance'),
]
