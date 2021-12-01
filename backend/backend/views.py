from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponseRedirect

from datetime import datetime, timedelta

from .utils import *
from task.models import *


def dashboard_news(keyword):
    news = request_selected_news(keyword)
    news_title_1 = news['articles'][0]['title']
    news_content_1 = news['articles'][0]['description']
    news_url_1 = news['articles'][0]['url']
    news_title_2 = news['articles'][1]['title']
    news_content_2 = news['articles'][1]['description']
    news_url_2 = news['articles'][1]['url']
    news_title_3 = news['articles'][2]['title']
    news_content_3 = news['articles'][2]['description']
    news_url_3 = news['articles'][2]['url']

    return news_title_1, news_title_2, news_title_3, news_content_1, news_content_2, news_content_3, news_url_1, news_url_2, news_url_3


def progress_count(request):
    unfinished_tasks = Task.objects.filter(owner=request.user, due__lte=datetime.today().replace(
        hour=23, minute=59, second=59), due__gte=datetime.today().replace(hour=23, minute=59, second=59) + timedelta(days=-7), complete_status=False)
    finished_tasks = Task.objects.filter(owner=request.user, due__lte=datetime.today().replace(
        hour=23, minute=59, second=59), due__gte=datetime.today().replace(hour=23, minute=59, second=59) + timedelta(days=-7),  complete_status=True)
    unfinished = len(unfinished_tasks)
    finished = len(finished_tasks)
    return unfinished, finished


def dashboard(request, task_id=None):

    unfinished, finished = progress_count(request)

    selected_symbol = '^GSPC'
    categoryData, values, last_high, last_close = request_selected_symbol(
        selected_symbol)

    keyword = 'stock'
    news_title_1, news_title_2, news_title_3, news_content_1, news_content_2, news_content_3, news_url_1, news_url_2, news_url_3 = dashboard_news(
        keyword)

    start_time = datetime.today().strftime('%Y-%m-%d')
    month = this_month()

    today = datetime.today().day

    Delaytask = Task.objects.filter(
        owner=request.user, due__lte=datetime.now(), complete_status=False)
    if len(Delaytask) > 0:
        delaynum = 'Warning!! '+str(len(Delaytask))+' Delayed task!'
    else:
        delaynum = ' Congratulations!! All Task finished on time!!'

    # create new issue
    instance = Task(owner=request.user)
    if task_id:
        instance = get_object_or_404(Task, pk=task_id)
    else:
        instance = Task(owner=request.user)

    form = TaskForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))

    tasks = Task.objects.filter(owner=request.user, due__lte=datetime.now(
    )+timedelta(days=1), complete_status=False).order_by('due').reverse()
    if len(tasks) >= 3:
        lastest_task1 = tasks[0]
        title1 = lastest_task1.title
        due1 = lastest_task1.due
        lastest_task2 = tasks[1]
        title2 = lastest_task2.title
        due2 = lastest_task2.due
        lastest_task3 = tasks[2]
        title3 = lastest_task3.title
        due3 = lastest_task3.due
    elif len(tasks) == 2:
        lastest_task1 = tasks[0]
        title1 = lastest_task1.title
        due1 = lastest_task1.due
        lastest_task2 = tasks[1]
        title2 = lastest_task2.title
        due2 = lastest_task2.due
        title3 = 'No Third task'
        due3 = 'No Third task'
    elif len(tasks) == 1:
        lastest_task1 = tasks[0]
        title1 = lastest_task1.title
        due1 = lastest_task1.due
        title2 = 'No Second task'
        due2 = 'No Second task'
        title3 = 'No Third task'
        due3 = 'No Third task'
    elif len(tasks) == 0:
        title1 = 'No First task'
        due1 = 'No First task'
        title2 = 'No Second task'
        due2 = 'No Second task'
        title3 = 'No Third task'
        due3 = 'No Third task'

    return render(request, 'Dashboard.html', locals())
