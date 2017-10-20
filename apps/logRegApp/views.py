from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages

##index page renders template w forms on it
def index(request):
    if 'user_id' not in request.session:
        return render(request, 'logRegApp/index.html')
    else:
        return redirect('/home')

def register(request):
    resp = User.objects.regValidation(request.POST) ##stores response you get from register method in manager
    if resp['status']: ##status is true or false whether there were messages or not
        user = User.objects.createUser(request.POST) ## creates user w data and stores their info into user variable
        request.session['user_id'] = user.id ##adds id to session
        return redirect('/home')
    else:
        for error in resp['errors']:
            messages.error(request,error)
        return redirect ('/')

def login(request):
    user = User.objects.login(request.POST) ##finds login method in User model and passes data into it
    if user:
        request.session['user_id'] = user.id ##if a user is returned, stores user id into session id method
        return redirect('/home') ##route to home page
    messages.error(request, 'Email or password is invalid') ## if no user found, flashes this error
    return redirect('/')

def home(request):
    data = {
        'userData': User.objects.get(id=request.session['user_id']) ##gets user data from db and stores in dictionary
    }
    return render(request, 'logRegApp/home.html', data)

def logout(request):
    request.session.clear() ##clears session
    return redirect('/')