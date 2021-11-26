import calendar
from datetime import date, datetime, timedelta
from pandas.core.tools import datetimes
import requests
import pandas as pd
from calendar import HTMLCalendar
from .models import Task

def this_monday():
    """
    Return the date of current week's monday.
    """
    today=date.today()
    return datetime.strftime(today-timedelta(today.weekday()),"%Y-%m-%d")

def this_month():
    today=date.today()
    return today.strftime('%B')

def this_year():
    today=date.today()
    return today.strftime('%Y')

def request_selected_symbol(selected_symbol):
    """
    Return the selected historical price data.
    """
    apikey="H1P717SYTFDWWWBK"
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+selected_symbol+'&apikey='+apikey
    r = requests.get(url)
    data = r.json()

    df=pd.DataFrame.from_dict(data['Time Series (Daily)'],orient='index').reset_index()
    df=df.rename(columns={'index':'date','1. open': 'open','2. high': 'high', '3. low': 'low','4. close': 'close','5. adjusted close':'adjusted close','6. volume':'volume','7. dividend amount':'dividend amount','8. split coefficient':'split coefficient'})
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['date'])
    df.open = df.open.astype(float)
    df.close = df.close.astype(float)
    df.high = df.high.astype(float)
    df.low = df.low.astype(float)

    return df

def request_selected_sma(selected_symbol):
    apikey="H1P717SYTFDWWWBK"
    url = 'https://www.alphavantage.co/query?function=SMA&symbol='+selected_symbol+'&interval=daily&time_period=10&series_type=close&apikey='+apikey
    r = requests.get(url)
    data = r.json()

    df=pd.DataFrame.from_dict(data['Technical Analysis: SMA'],orient='index').reset_index()
    df=df.rename(columns={'index':'date'})
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['date'])
    df.SMA = df.SMA.astype(float)

    return df

def small_calendar():
    today=date.today()
    tc=HTMLCalendar(calendar.SUNDAY).formatmonth(today.year,today.month)
    table=tc.splitlines()
    table.pop(1)

    return '\n'.join(table)

def request_selected_news(keyword):
    """
    """
    url = ('https://newsapi.org/v2/everything?'
       'q='+keyword+'&'
       'sortBy=publishedAt&'
       'apiKey=6e63bd2af1fb4b5b9df13be0810cb70f')
    r=requests.get(url)
    news=r.json()

    return news

#print(request_selected_news('AAPL AND stock'))

class Calendar(HTMLCalendar):
    def _init_(self, year=None, month=None):
        self.year =  year
        self.month = month
        super(Calendar, self).__init__()

    # Transform the days into td
    def Transday(self, day, tasks):
        tasks_today = tasks.filter(due_time__day = day)
        day_tr = ''
        for task in tasks_today:
            day_tr += f'<li>{task.Issue}</li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {day_tr} </ul></td>"
        return '<td></td>'
    
    # Transform a week into tr
    def Transweek(self, weekdays, tasks):
        week = ''
        for day, weekday in weekdays:
            week+=self.Transday(day,tasks)
        return f'<tr>{week}</tr>'

    # Transform a month into table
    def Transmonth(self, withyear=True):
        tasks = Task.objects.filter(
            due_time__year=self.year, due_time__month = self.month)

        month = f'<table  border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        month += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        month += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year,self.month):
            month += f'{self.Transweek(week,tasks)}\n'
        return month

            


