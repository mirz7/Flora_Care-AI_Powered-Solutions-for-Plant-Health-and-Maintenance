from rest_framework import serializers
from .models import Plant, Device, SensorData, DeviceCommand

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = '__all__'

class DeviceCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceCommand
        fields = '__all__'

# Django URLs (urls.py)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'plants', views.PlantViewSet)
router.register(r'devices', views.DeviceViewSet)
router.register(r'plant-data', views.SensorDataViewSet)
router.register(r'commands', views.DeviceCommandViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]