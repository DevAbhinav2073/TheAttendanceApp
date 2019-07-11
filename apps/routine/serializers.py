from datetime import datetime

from rest_framework import serializers

from apps.constants import DAY_LIST
from apps.information.serializers import ProgrammeSerializer
from apps.routine.models import RoutineDetail, Routine, ClassAttendingDetail


class RoutineSerializer(serializers.ModelSerializer):
    programme = ProgrammeSerializer()

    class Meta:
        model = Routine
        fields = '__all__'


class RoutineDetailSerializer(serializers.ModelSerializer):
    routine_of = RoutineSerializer()
    day_of_week = serializers.SerializerMethodField()
    corrected_from_time = serializers.SerializerMethodField()
    corrected_to_time = serializers.SerializerMethodField()
    is_attending = serializers.SerializerMethodField()
    is_cancelled = serializers.SerializerMethodField()

    def get_is_attending(self, obj):
        return obj.is_attending(self.date)

    def get_day_of_week(self, obj):
        return DAY_LIST[obj.day_of_week]

    def get_is_cancelled(self, obj):
        return obj.is_cancelled(self.date)

    #
    def get_corrected_from_time(self, obj):
        return obj.corrected_from_time(self.date)

    #
    def get_corrected_to_time(self, obj):
        return obj.corrected_to_time(self.date)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date = self.context.get('date', datetime.now().date)

    class Meta:
        model = RoutineDetail
        fields = '__all__'


class ClassAttendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassAttendingDetail
        fields = '__all__'

