from rest_framework import serializers
from echo.models import Data,Element,Device

class ElementSerializer(serializers.ModelSerializer):
    #device=serializers.PrimaryKeyRelatedField(queryset=Device.objects.all())
    class Meta:
        model = Element
        fields = '__all__'

"""
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

"""

class DataSerializer(serializers.ModelSerializer):
    element = ElementSerializer(many=True)    
    class Meta:
        model = Data
        #fields = '__all__'
        fields = ['data_id', 'element', 'record_time']