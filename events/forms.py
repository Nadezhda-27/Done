from django.forms import ModelForm
from .models import Events

class EventsForm(ModelForm):
    class Meta:
        model = Events
        fields = ['title', 'memo', 'important']