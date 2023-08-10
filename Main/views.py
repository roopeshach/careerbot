from django.shortcuts import render, redirect
from .models import CareerAssesmentAnswer, CareerAssesmentQuestion
from django.conf import settings
from .secret_key import API_KEY
import openai, json
openai.api_key = API_KEY
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
# views.py
from .forms import CareerAssessmentForm
from .models import CareerAssessmentResponse
from django.contrib import messages


# Create your views here.
@login_required
def index(request):
    # request.session.flush()
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



@login_required
def career_assessment(request):
    if request.method == 'POST':
        #if previous response dont add
        user = request.user
        career_responses = get_user_response(user)
        if career_responses != "":
            messages.error(request, 'You have already submitted your career assessment, delete previous for adding new.')
            return redirect('Main:career-assesment')
        #else save new
        else:
            form = CareerAssessmentForm(request.POST)
            if form.is_valid():
                user = request.user  # Assuming you have a logged-in user
                responses = {}
                for question_id, answer_id in form.cleaned_data.items():
                    question = CareerAssesmentQuestion.objects.get(id=question_id.split('_')[1])
                    answer = CareerAssesmentAnswer.objects.get(id=answer_id)
                    responses[question.question] = answer.answer  # Store the answer text
                response_json = json.dumps(responses)  # Convert responses to JSON
                CareerAssessmentResponse.objects.create(user=user, responses=response_json)
                messages.success(request, 'Your career assessment has been submitted successfully.')
                return redirect('Main:career-assesment')  # Redirect to a success page
    else:
        form = CareerAssessmentForm()

        #if previous response fetch it 
        user = request.user
        career_responses = get_user_response(user)
        if career_responses != "":
            career_responses = json.loads(career_responses)
        else:
            career_responses = {}


        questions = CareerAssesmentQuestion.objects.filter(is_active=True)
        context = {
            'form': form,
            'questions': questions,
            'career_responses': career_responses,
        }
        return render(request, 'Main/career_assessment.html', context)




def get_user_response(user):
    try:
        career_responses = CareerAssessmentResponse.objects.filter(user=user).latest('created_at')
        career_responses = career_responses.responses
    except CareerAssessmentResponse.DoesNotExist:
        career_responses = ""
    return career_responses

@login_required
def delete_user_assesment(request):
    user = request.user
    career_responses = CareerAssessmentResponse.objects.filter(user=user)
    # if exists delete if dont show message
    if career_responses.exists():
        career_responses.delete()
        messages.success(request, 'Your career assessment has been deleted successfully.')
    else:
        messages.success(request, 'No career assessment to delete.')
    return redirect('Main:career-assesment')

# This method formats the user responses as HTML for display
def format_responses_as_html(responses):
    html = ""
    for question, answer in responses.items():
        html += f"<strong>{question}</strong>: {answer}<br>"
    return html

# Initialize the ChatGPT model
openai.api_key = "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"

# This method initializes the chatbot and returns the chatbot's response
def initialize_chatbot(prompt_data, choice):
    choices = [
        'career_suggestion',
        'industry_insights',
        'interview_tips',
        'resume_tips'
    ]

    if choice.strip() not in choices:
        raise Exception('Invalid choice.')

    # Define the initial message for each choice
    initial_messages = {
        'career_suggestion': "You are a career suggestion bot. Your goal is to provide career suggestions based on the user's responses to career assessment questions. Here are the user's responses: Note(Provide output in html formatted tags.",
        'industry_insights': "You are an industry insights bot. Your goal is to provide industry insights based on the user's responses to career assessment questions. Here are the user's responses: Note(Provide output in html formatted tags. Note(Provide output in html formatted tags.",
        'interview_tips': "You are an interview tips bot. Your goal is to provide interview tips based on the user's responses to career assessment questions. Here are the user's responses: Note(Provide output in html formatted tags.",
        'resume_tips': "You are a resume tips bot. Your goal is to provide resume tips based on the user's responses to career assessment questions. Here are the user's responses: Note(Provide output in html formatted tags."
    }

    initial_message = initial_messages[choice.strip()]
    formatted_responses = format_responses_as_html(json.loads(prompt_data))
    prompt = f"{initial_message}<br><br>{formatted_responses}"

    # Set up and invoke the ChatGPT model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a chatbot that assists with career-related questions."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.5,
    )

    return response.choices[0].message['content']


# Career Suggestion Chatbot View
@login_required
def career_suggestion_chatbot_view(request, choice):
    # Define valid choices
    valid_choices = ['career_suggestion', 'industry_insights', 'interview_tips', 'resume_tips']

    if choice not in valid_choices:
        return redirect('Main:home')  # Redirect to home or some other page if the choice is not valid

    # Set the session variable for the selected choice
    request.session['selected_choice'] = choice

    # Get the user's career assessment responses
    career_responses = get_user_response(request.user)

    # Get the current conversation for the selected choice from session
    conversation_key = f'{choice}_conversation'
    conversation = request.session.get(conversation_key, [])

    if request.method == 'POST':
        user_input = request.POST.get('user_input')

        # Append user input to the conversation
        if user_input:
            conversation.append({"role": "user", "content": user_input})

        # Format prompts for the chatbot
        prompts = [{"role": message["role"], "content": message["content"]} for message in conversation]

        # Set up and invoke the ChatGPT model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompts,
            api_key=openai.api_key,
            temperature=0.5,
            max_tokens=100
        )

        # Extract chatbot replies from the response
        chatbot_replies = [message['message']['content'] for message in response['choices'] if message['message']['role'] == 'assistant']

        # Append chatbot replies to the conversation
        for reply in chatbot_replies:
            conversation.append({"role": "assistant", "content": reply})

        # Update the conversation in the session
        request.session[conversation_key] = conversation

        return render(request, 'Main/chat.html', {'user_input': user_input, 'chatbot_replies': chatbot_replies, 'conversation': conversation})
    else:
        try:
            # Load the previous conversation from session if exists
            conversation = request.session[conversation_key]
            return render(request, 'Main/chat.html', {'conversation': conversation})
        except KeyError:
            # If previous conversation does not exist, initialize the chatbot with prompt
            if career_responses:
                # Initialize chatbot with prompt
                chatbot_prompt = initialize_chatbot(career_responses, choice)
                conversation.append({"role": "assistant", "content": chatbot_prompt})
                request.session[conversation_key] = conversation
                return render(request, 'Main/chat.html', {'conversation': conversation})
            else:
                # Add message and redirect
                messages.success(request, 'Please complete the career assessment first.')
                return redirect('Main:career-assessment')