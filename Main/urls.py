from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('data/', views.upload_career_assessment_data, name="upload_career_assessment_data"),
    path('career-assesment', views.career_assessment, name='career-assesment'),
    path('delete-user-assesment', views.delete_user_assesment, name="delete_user_assesment"),
    path('chat/<str:choice>', views.career_suggestion_chatbot_view, name="chat"),
]
