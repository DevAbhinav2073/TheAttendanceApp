from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from apps.authuser.models import *

User = get_user_model()


class StudentDetailSerializer(serializers.ModelSerializer):
    programme_name = serializers.SerializerMethodField()

    def get_programme_name(self, obj):
        return obj.programme.name

    class Meta:
        model = StudentDetail
        exclude = ('id', 'user', 'programme')


class TeacherDetailSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()

    def get_department_name(self, obj):
        if obj.department:
            return obj.department.name

    class Meta:
        model = TeacherDetail
        exclude = ()


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    student_detail = StudentDetailSerializer()
    teacher_detail = TeacherDetailSerializer()

    def get_token(self, obj):
        obj, _ = Token.objects.get_or_create(user=obj)
        return obj.key

    class Meta:
        model = User
        fields = (
            'id', 'username', 'user_type', 'image', 'token', 'student_detail', 'teacher_detail')
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'student_detail': {
                'read_only': True
            },
            'teacher_detail': {
                'read_only': True
            }
        }


class FeedbackSerializer(serializers.ModelSerializer):
    teacher_name = serializers.SerializerMethodField()
    feedback_by_name = serializers.SerializerMethodField()

    def get_teacher_name(self, obj):
        try:
            return obj.teacher.teacher_detail.name
        except:
            return 'None'

    def get_feedback_by_name(self, obj):
        try:
            return obj.feedback_by.student_detail.name
        except:
            return 'None'

    class Meta:
        model = Feedback
        fields = '__all__'
