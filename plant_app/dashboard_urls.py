from django.urls import path
from . import views

# URL patterns for the web interface
urlpatterns = [
    # Dashboard route
    path('', views.dashboard, name='dashboard'),
    
    # Device detail route
    path('device/<str:device_id>/', views.device_detail, name='device_detail'),
]