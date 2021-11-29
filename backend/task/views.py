from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.html import format_html
from django.views import generic
from django.utils.safestring import mark_safe
from django.urls import reverse

from .models import *
from backend.utils import this_month, this_year, small_calendar
from .utils import Calendar

from datetime import date, datetime, time, timedelta
import calendar

# Create your views here.


class CalendarView(generic.ListView):
    model = Task
    template_name = 'Calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['this_month'] = this_month()
        context['this_year'] = this_year()
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['sidebar_dates'] = sidebar_calendar()
        context['sidebar_today'] = datetime.today().strftime('%d/%m/%Y')

        return context


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def task(request, task_id=None):
    instance = Task()
    if task_id:
        instance = get_object_or_404(Task, pk=task_id)
    else:
        instance = Task()

    form = TaskForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'Task.html', {'form': form})


def sidebar_calendar():
    today = datetime.today()
    sidebar_dates = [[] for i in range(6)]

    tmp = date(today.year,today.month,day=1)
    for i in range(6):
        for j in range(7):
            if j == tmp.weekday() and tmp.month == today.month:
                sidebar_dates[i].append(tmp.day)
                tmp += timedelta(days=1)
            else:
                sidebar_dates[i].append('')

    return sidebar_dates
