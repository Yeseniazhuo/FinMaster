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
from django.urls import path, include
from django.contrib.auth.decorators import login_required

from . import views
from login.views import login, register, logout
from task.views import CalendarView, task
from finance.views import user_settings, info

import debug_toolbar


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(views.dashboard)),
    path('calendar/', login_required(CalendarView.as_view()), name='calendar'),
    path('info/', login_required(info), name='info'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('settings/', login_required(user_settings), name='settings'),
    path('task/new/', login_required(task), name='task_new'),
    path('task/edit/(?P<task_id>\d+)/$', login_required(task), name='task_edit'),
    path('__debug__/', include(debug_toolbar.urls)), # for performance test
]
