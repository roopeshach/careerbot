from django.contrib import admin

# Register your models here.
from .models import  CareerSuggestion, Resume, InterviewTip, IndustryInsight, UserFeedback, CareerAssesmentQuestion, CareerAssesmentAnswer, CareerAssessmentResponse
from django.utils.html import format_html

admin.site.register(CareerSuggestion)
admin.site.register(Resume)
admin.site.register(InterviewTip)
admin.site.register(IndustryInsight)
admin.site.register(UserFeedback)

class CareerAssementAnswerTablularInline(admin.TabularInline):
    model = CareerAssesmentAnswer
    extra = 1

class CareerAssesmentQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active', 'created_at', 'answers')
    list_filter = ('is_active', 'created_at')
    search_fields = ('question',)

    inlines = [CareerAssementAnswerTablularInline]

    def answers(self, obj):
        return format_html("<br>".join([answer.answer for answer in obj.careerassesmentanswer_set.all()]))
    
admin.site.register(CareerAssesmentQuestion, CareerAssesmentQuestionAdmin)


class CareerAssementQuestionTabularInline(admin.TabularInline):
    model = CareerAssesmentQuestion
    extra = 1

class CareerAssesmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer')
    list_filter = ('user', 'question', 'answer')
    search_fields = ('user', 'question', 'answer')

    # inlines = [CareerAssementQuestionTabularInline]


admin.site.register(CareerAssessmentResponse)

