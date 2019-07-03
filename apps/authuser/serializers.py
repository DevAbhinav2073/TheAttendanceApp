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
            'username', 'first_name', 'last_name', 'email', 'user_type', 'token', 'student_detail', 'teacher_detail')
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
