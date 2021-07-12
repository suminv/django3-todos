from django.shortcuts import redirect, render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate



def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    """
    создание нового пользователя. При GET запросе отобращаем форму, при POST делаем проверки на одинаковый пароль, после этого создается новый пользоваталь, который попадает на свою страницу.
    """
    if request.method == "GET":
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'], 
                    password=request.POST['password1']
                    )
                user.save()
                # перенаправление на свою страницу
                login(request, user)
                return redirect('currenttodos')

            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'That username has already been taken. Please choose a new username.'})

        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Password did not match.'})


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def loginuser(request):
    if request.method == "GET":
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username end password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')


def currenttodos(request):
    return render(request, 'todo/currenttodos.html')
