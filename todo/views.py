from todo.models import Todo
from django.shortcuts import redirect, render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm 
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


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

@login_required
def logoutuser(request):
    """
    @login_required только для зарегистрированных пользователей
    """
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

@login_required
def currenttodos(request):
    """
    Отображает записи, конкретного пользователя.
    filter проверяем имя пользователя с автором заметки

    """
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})


@login_required
def viewtodo(request, todo_pk):
    """
    - сравнивает ключ записи (pk)
    - сравнивает user
    - instance=todo обозначает, что мы изменяем объект, а не создаем новый
    """
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user )
    
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error': 'Bad info.'})

@login_required
def completetodo(request, todo_pk):
    """
    Завершение задачи. Убедиться, что запрос имеет POST и завершить задачу.
    """
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    """
    Удаление задачи. Убедиться, что запрос имеет POST и завершить задачу.
    """
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')


def completedtodos(request):
    """
    datecompleted__isnull проверка даты заполнения
    """
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completedtodos.html', {'todos': todos})
    

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            # делаем привязку к конкретному user
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error': 'Bad data passed in. Try again.'})
