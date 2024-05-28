from django.forms import ModelForm
from .models import Todo
from .models import Category

class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'memo', 'important', 'deadline', 'category']

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']