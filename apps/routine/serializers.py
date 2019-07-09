from rest_framework import serializers

from apps.information.serializers import ProgrammeSerializer
from apps.routine.models import RoutineDetail, Routine


class RoutineSerializer(serializers.ModelSerializer):
    programme = ProgrammeSerializer()

    class Meta:
        model = Routine
        fields = '__all__'


class RoutineDetailSerializer(serializers.ModelSerializer):
    routine_of = RoutineSerializer()

    class Meta:
        model = RoutineDetail
        fields = '__all__'
