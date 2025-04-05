# from django.urls import path
# from . import views

# app_name = 'plant_disease_app' 

# # urlpatterns = [
# #     path('plant_disease/', views.home_page, name='home'),
# #     path('index/', views.ai_engine_page, name='index'),
# #     path('submit/', views.submit, name='submit'),
# # ]

# # urlpatterns = [
# #     path('', views.home_page, name='plant_disease_home'),  # This will render index.html
# #     path('submit/', views.submit_page, name='plant_disease_submit'),  # This will render submit.html
# # ]

# urlpatterns = [
#     path('index/', views.index, name='index'),
#     path('submit/', views.submit, name='submit'),
# ]

from django.urls import path
from . import views
from plant_disease_app.views import ai_engine 


app_name = 'plant_disease_app'

urlpatterns = [
    
    path('ai-engine/', views.ai_engine, name='ai_engine'),
    path('submit/', views.submit, name='submit'),
]