import calendar
from datetime import date, datetime, timedelta
from pandas.core.tools import datetimes
import requests
import pandas as pd
from calendar import HTMLCalendar

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


