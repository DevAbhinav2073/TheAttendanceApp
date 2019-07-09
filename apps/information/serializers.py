from rest_framework import serializers

from apps.information.models import Programme


class ProgrammeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programme
        fields = '__all__'
