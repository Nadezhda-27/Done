"""Done URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from account.views import *
from notes.views import *
from todo.views import *
from events.views import *

todo_router = routers.SimpleRouter()
todo_router.register(r'all_todos', TodoViewSet)

urlpatterns = [
    # API
    path('api/', include(todo_router.urls)),
    # Healthcheck
    path('healthcheck', healthcheck, name='healthcheck'),
    # Admin
    path('admin/', admin.site.urls),
    # Auth
    path('signup/', signup_user, name='signup_user'),
    path('logout/', logout_user, name='logout_user'),
    path('login/', login_user, name='login_user'),
    # Todos
    path('create_todo/', create_todo, name='create_todo'),
    path('current_todos/', current_todos, name='current_todos'),
    path('completed_todos/', completed_todos, name='completed_todos'),
    path('todo/<int:todo_pk>', view_todo, name='view_todo'),
    path('todo/<int:todo_pk>/complete', complete_todo, name='complete_todo'),
    path('todo/<int:todo_pk>/delete', delete_todo, name='delete_todo'),
    path('', home, name='home'),
    path('categories/create/', create_category, name='create_category'),
    path('categories/', manage_categories, name='manage_categories'),
    path('categories/<int:category_pk>/edit/', edit_category, name='edit_category'),
    path('categories/<int:category_pk>/delete/', delete_category, name='delete_category'),

    # Notes
    path('create_note/', create_note, name='create_note'),
    path('notes_list/', notes_list, name='notes_list'),
    path('notes_list/<int:note_id>', note_detail, name='note_detail'),
    path('notes_list/<int:note_id>/delete', delete_note, name='delete_note'),

    # Events
    path('create_events/', create_events, name='create_events'),
    path('current_events/', current_events, name='current_events'),
    path('completed_events/', completed_events, name='completed_events'),
    path('events/<int:events_pk>', view_events, name='view_events'),
    path('events/<int:events_pk>/complete', complete_events, name='complete_events'),
    path('events/<int:events_pk>/delete', delete_events, name='delete_events'),
    path('events_json/', events_json, name='events_json'),

]
