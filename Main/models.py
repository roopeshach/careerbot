from django.db import models
from django.contrib.auth.models import User

class CareerAssesmentQuestion(models.Model):
    question = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CareerAssesmentAnswer(models.Model):
    answer = models.CharField(max_length=255)
    question = models.ForeignKey(CareerAssesmentQuestion, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CareerAssessmentResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    responses = models.TextField()  # Store responses as JSON or text format
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username    }'s Career Assessment Response"

#models to store chat of careersuggesstion 
class CareerSuggesstionChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_ai = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username}'s Chat"
    
#models to store chat of industryinsights
class IndustryInsightsChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_ai = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username}'s Chat"
    
#models to store chat of interviewtips
class InterviewTipsChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_ai = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username}'s Chat"
    
#models to store chat of resumetips
class ResumeTipsChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_ai = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username}'s Chat"
    
    