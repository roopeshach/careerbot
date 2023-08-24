# forms.py
from django import forms
from .models import CareerAssesmentQuestion, CareerSuggesstionChat, IndustryInsightsChat, InterviewTipsChat, ResumeTipsChat
class CareerAssessmentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        questions = CareerAssesmentQuestion.objects.filter(is_active=True)
        for question in questions:
            answers = question.careerassesmentanswer_set.all()
            choices = [(answer.id, answer.answer) for answer in answers]
            self.fields[f"question_{question.id}"] = forms.ChoiceField(
                choices=choices, widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
            )

class CareerSuggesstionChatForm(forms.ModelForm):
    class Meta:
        model = CareerSuggesstionChat
        fields = ['message']

class IndustryInsightsChatForm(forms.ModelForm):
    class Meta:
        model = IndustryInsightsChat
        fields = ['message']

    
class InterviewTipsChatForm(forms.ModelForm):
    class Meta:
        model = InterviewTipsChat
        fields = ['message']

class ResumeTipsChatForm(forms.ModelForm):
    class Meta:
        model = ResumeTipsChat
        fields = ['message']

        