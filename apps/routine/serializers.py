from rest_framework import serializers

from apps.routine.models import RoutineDetail


class RoutineDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineDetail
        fields = '__all__'
