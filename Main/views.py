from django.shortcuts import render
from .models import CareerAssesmentAnswer, CareerAssesmentQuestion
from django.conf import settings
# Create your views here.
def index(request):
    return render(request, 'Main/index.html')

import json

def upload_career_assessment_data(request):
    with open(str(settings.BASE_DIR) + "/data.json", "r") as f:
        data = json.load(f)

    for question_data in data["questions"]:
        question = CareerAssesmentQuestion.objects.create(
            question=question_data["question"],
            is_active=True
        )

        for answer_text in question_data["answers"]:
            answer = CareerAssesmentAnswer.objects.create(
                question=question,
                answer=answer_text,
                is_active=True
            )

    print("Career assessment data uploaded successfully.")

    return render(request, 'Main/index.html')

def career_assessment(request):
    questions = CareerAssesmentQuestion.objects.filter(is_active=True)
    context = {
        'questions': questions,
    }
    return render(request, 'Main/career_assessment.html', context)

