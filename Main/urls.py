from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('data/', views.upload_career_assessment_data, name="upload_career_assessment_data"),
]
