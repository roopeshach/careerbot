from django.shortcuts import render, redirect
from .models import CareerAssesmentAnswer, CareerAssesmentQuestion
from django.conf import settings
from .secret_key import API_KEY
import openai
openai.api_key = API_KEY

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



# this is the home view for handling home page logic
def home(request):
    try:
        # if the session does not have a messages key, create one
        if 'messages' not in request.session:
            request.session['messages'] = [
                {"role": "system", "content": "You are now chatting with a user, provide them with comprehensive, short and concise answers."},
            ]
        if request.method == 'POST':
            # get the prompt from the form
            prompt = request.POST.get('prompt')
            # get the temperature from the form
            temperature = float(request.POST.get('temperature', 0.1))
            # append the prompt to the messages list
            request.session['messages'].append({"role": "user", "content": prompt})
            # set the session as modified
            request.session.modified = True
            # call the openai API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=request.session['messages'],
                temperature=temperature,
                max_tokens=1000,
            )
            # format the response
            formatted_response = response['choices'][0]['message']['content']
            # append the response to the messages list
            request.session['messages'].append({"role": "assistant", "content": formatted_response})
            request.session.modified = True
            # redirect to the home page
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': temperature,
            }
            return render(request, 'Main/home.html', context)
        else:
            # if the request is not a POST request, render the home page
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': 0.1,
            }
            return render(request, 'Main/home.html', context)
    except Exception as e:
        print(e)
        # if there is an error, redirect to the error handler
        return redirect('Main:error_handler')

def new_chat(request):
    # clear the messages list
    request.session.pop('messages', None)
    return redirect('Main:home')


# this is the view for handling errors
def error_handler(request):
    return render(request, 'Main/404.html')


def chat(request):
    return render(request, 'Main/chat.html')