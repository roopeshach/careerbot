# forms.py
from django import forms
from .models import CareerAssesmentQuestion

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
