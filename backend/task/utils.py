from calendar import HTMLCalendar
from .models import Task


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # Transform the days into td
    def formatday(self, day, tasks):
        tasks_today = tasks.filter(due__day=day, complete_status=False)
        day_tr = ''
        for task in tasks_today:
            day_tr += f'<li>{task.get_html_url}</li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {day_tr} </ul></td>"
        return '<td></td>'

    # Transform a week into tr
    def formatweek(self, weekdays, tasks):
        week = ''
        for day, weekday in weekdays:
            week += self.formatday(day, tasks)
        return f'<tr>{week}</tr>'

    # Transform a month into table
    def formatmonth(self, withyear=True):
        tasks = Task.objects.filter(
            due__year=self.year, due__month=self.month)

        month = f'<table  border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        month += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        month += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            month += f'{self.formatweek(week,tasks)}\n'
        return month
