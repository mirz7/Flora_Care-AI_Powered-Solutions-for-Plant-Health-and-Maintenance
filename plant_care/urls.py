from django.urls import path
from django.conf import settings  # Add this import
from django.conf.urls.static import static
from . import views

app_name = 'plant_care'  # Required for namespace in include()


urlpatterns = [
    path('', views.plant_care_home, name='plant_care_home'),
    path('generate_care_guide/', views.generate_care_guide, name='generate_care_guide'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
