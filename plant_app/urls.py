from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Set up DRF router for automatic URL routing
router = DefaultRouter()
router.register(r'plants', views.PlantViewSet)
router.register(r'devices', views.DeviceViewSet)
router.register(r'sensor-data', views.SensorDataViewSet)
router.register(r'device-commands', views.DeviceCommandViewSet)

app_name = 'plant_app' 

urlpatterns = [
    # Web interface URLs
   
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # API endpoints for ESP32 devices
    path('plant-data/', views.receive_plant_data, name='receive_plant_data'),
    path('plant-data/commands/<str:device_id>/', views.device_commands, name='device_commands'),
    
    # AJAX endpoints for web interface
    path('device/<str:device_id>/commands/water/', views.send_water_command, name='send_water_command'),
    path('device/<str:device_id>/commands/settings/', views.update_settings, name='update_settings'),
    path('device/<str:device_id>/commands/data/', views.get_device_data, name='get_device_data'),
    path('device/<str:device_id>/', views.device_detail, name='device_detail'),
    
    # Include DRF router URLs
    path('api/', include(router.urls)),
    path('test/', views.test_view, name='test_view'),
]