from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .forms import EventsForm
from .models import Events
# from .serializers import EventsSerializer


# class EventsViewSet(viewsets.ModelViewSet):
#     queryset = Events.objects.all()
#     # serializer_class = EventsSerializer
#     permission_classes = (IsAdminUser,)


# def healthcheck(request):
#     return JsonResponse({'status': 'ok'})


# def home(request):
#     if request.user.is_authenticated:
#         return redirect('current_events')
#     else:
#         return render(request, 'events/home.html')


@login_required
def create_events(request):
    if request.method == 'GET':
        return render(request, 'create_events.html', {'form': EventsForm()})
    else:
        try:
            form = EventsForm(request.POST)
            new_events = form.save(commit=False)
            new_events.user = request.user
            new_events.save()
            return redirect('current_events')
        except ValueError:
            return render(request, 'create_events.html', {'form': EventsForm(), 'error': 'Bad data passed in'})


@login_required
def complete_events(request, events_pk):
    events = get_object_or_404(Events, pk=events_pk, user=request.user)
    if request.method == 'POST':
        events.datecompleted = timezone.now()
        events.save()
        return redirect('current_events')


@login_required
def delete_events(request, events_pk):
    events = get_object_or_404(Events, pk=events_pk, user=request.user)
    if request.method == 'POST':
        events.delete()
        return redirect('current_events')


@login_required
def view_events(request, events_pk):
    events = get_object_or_404(Events, pk=events_pk, user=request.user)
    if request.method == 'GET':
        form = EventsForm(instance=events)
        return render(request, 'view_events.html', {'events': events, 'form': form})
    else:
        try:
            form = EventsForm(request.POST, instance=events)
            form.save()
            return redirect('current_events')
        except ValueError:
            return render(request, 'view_events.html', {'events': events, 'form': form, 'error': 'Bad info'})


@login_required
def current_events(request):
    events = Events.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'current_events.html', {'events': events})



@login_required
def completed_events(request):
    events = Events.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'completed_events.html', {'events': events})