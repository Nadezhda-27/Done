from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .forms import TodoForm
from .models import Todo, Category
from .serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = (IsAdminUser,)


def healthcheck(request):
    return JsonResponse({'status': 'ok'})


def home(request):
    if request.user.is_authenticated:
        return redirect('current_todos')
    else:
        return render(request, 'todo/home.html')


@login_required
def create_todo(request):
    categories = Category.objects.all()
    if request.method == 'GET':
        return render(request, 'todo/create_todo.html', {'form': TodoForm(), 'categories': categories})
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo/create_todo.html', {'form': TodoForm(), 'categories': categories, 'error': 'Bad data passed in'})

@login_required
def complete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('current_todos')


@login_required
def delete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('current_todos')


@login_required
def view_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    categories = Category.objects.all()
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/view_todo.html', {'todo': todo, 'form': form, 'categories': categories})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo/view_todo.html', {'todo': todo, 'form': form, 'categories': categories, 'error': 'Bad info'})



@login_required
def current_todos(request):
    category_id = request.GET.get('category', 'all')
    if category_id == 'all':
        todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True).order_by('deadline')
    else:
        todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True, category_id=category_id).order_by('deadline')
    categories = Category.objects.all()
    return render(request, 'todo/current_todos.html', {'todos': todos, 'categories': categories, 'selected_category': category_id})


@login_required
def completed_todos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completed_todos.html', {'todos': todos})
