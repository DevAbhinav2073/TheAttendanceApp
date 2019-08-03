from rest_framework import serializers

from .models import *


class MarksDetailSerializer(serializers.ModelSerializer):
    year = serializers.SerializerMethodField()
    part = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    # programme = serializers.SerializerMethodField()
    th_pr = serializers.SerializerMethodField()
    # batch = serializers.SerializerMethodField()
    full_marks = serializers.SerializerMethodField()

    def get_full_marks(self, obj):
        return obj.marks_instance.full_mark

    def get_year(self, obj):
        return obj.marks_instance.year

    def get_part(self, obj):
        return obj.marks_instance.part

    def get_subject(self, obj):
        return obj.marks_instance.subject.name

    def get_programme(self, obj):
        return obj.marks_instance.programme.name

    def get_th_pr(self, obj):
        return obj.marks_instance.theory_practical

    def get_batch(self, obj):
        return obj.marks_instance.batch

    class Meta:
        model = MarksDetail
        fields = ('year', 'part', 'subject', 'th_pr', 'marks', 'full_marks')
