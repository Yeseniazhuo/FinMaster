"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from . import views
from login.views import login, register, logout
from task.views import CalendarView, task

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard),
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('info/', views.info, name='info'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('task/new/', task, name='task_new'),
    path('task/edit/(?P<task_id>\d+)/$', task, name='task_edit'),
]
