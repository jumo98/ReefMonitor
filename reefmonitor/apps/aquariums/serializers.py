from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from .models import Aquarium, Measurement, Parameter

class AquariumSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=24)
    owner = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )
    id = serializers.CharField(max_length=100)
    create_date = serializers.DateTimeField()
    update_date = serializers.DateTimeField()

    class Meta:
        model = Aquarium
        fields = ('__all__')

class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('name', 'value')

class MeasurementSerializer(WritableNestedModelSerializer):
    timestamp = serializers.DateTimeField()
    parameters = ParameterSerializer(many=True)

    class Meta:
        model = Measurement
        fields = ('timestamp','parameters')



