from django.db import models
from django.contrib.auth.models import User

class CareerAssessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

class CareerSuggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    suggestion = models.CharField(max_length=255)

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

class InterviewTip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tip = models.TextField()

class IndustryInsight(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    industry = models.CharField(max_length=255)
    job_roles = models.TextField()
    future_prospects = models.TextField()

class UserFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField()
