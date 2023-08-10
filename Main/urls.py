from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('data/', views.upload_career_assessment_data, name="upload_career_assessment_data"),
    path('career-assesment', views.career_assessment, name='career-assesment'),
    path('new_chat/', views.new_chat, name='new_chat'),
    path('error-handler/', views.error_handler, name='error_handler'),
    path('home', views.home, name='home'),
    path('chat', views.chat, name="chat")
    
]
