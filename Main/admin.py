from django.contrib import admin

# Register your models here.
from .models import CareerAssessment, CareerSuggestion, Resume, InterviewTip, IndustryInsight, UserFeedback


admin.site.register(CareerAssessment)
admin.site.register(CareerSuggestion)
admin.site.register(Resume)
admin.site.register(InterviewTip)
admin.site.register(IndustryInsight)
admin.site.register(UserFeedback)