from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from .forms import UserForm 
from django.contrib.auth.models import User
# Create your views here.
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=request.POST.get('username'))
            login(request, user)
            messages.success(request, 'Staff User registered successfully. Please login to continue.')
            return redirect('/register')
            
        else:
            print(form.errors)
            context = {
                'error' : form.errors,
            }
            return render(request, 'authentication/register.html', context)
    else:
        return render(request, 'authentication/register.html')

def login_user(request):
    if request.user.is_authenticated:
        return redirect('Main:index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('Main:index')
                
            else:
                context = {
                    'error': "User credentials don't match!!"
                }
                return render(request, 'authentication/login.html', context)
        else:  
            return render(request, 'authentication/login.html')

#logout
def logout_user(request):

    logout(request)
    return redirect('authentication:login')


