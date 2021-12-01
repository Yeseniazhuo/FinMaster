from datetime import date
import requests
import yfinance as yf


def this_month():
    today = date.today()
    return today.strftime('%B')


def this_year():
    today = date.today()
    return today.strftime('%Y')


def request_selected_symbol(selected_symbol, inr="1d"):
    s = yf.Ticker(selected_symbol)

    if inr == "1d" or inr == "1day":
        inr = "1d"
        pd = "3mo"
        dt_format = '%y/%m/%d'
    elif inr == "1h" or inr == "1hour":
        inr = "1h"
        pd = "1mo"
        dt_format = '%m/%d %H'
    elif inr == "5m" or inr == "5mins":
        inr = "5m"
        pd = "5d"
        dt_format = '%m/%d %H:%M'
    elif inr == "1m" or inr == "1min":
        inr = "1m"
        pd = "1d"
        dt_format = '%m/%d %H:%M'

    s_historical = s.history(period=pd, interval=inr, actions=False).reindex(
        columns=['Open', 'Close', 'Low', 'High'])
    categoryData = []
    values = []
    for index, data in s_historical.iterrows():
        categoryData.append(index.strftime(dt_format))
        values.extend(data.values)

    last_high = round(s_historical.iloc[-1]['High'], 2)
    last_close = round(s_historical.iloc[-1]['Close'], 2)

    return categoryData, values, last_high, last_close


def request_selected_news(keyword):
    """
    """
    url = ('https://newsapi.org/v2/everything?'
           'q='+keyword+'&'
           'sortBy=publishedAt&apiKey=6e63bd2af1fb4b5b9df13be0810cb70f&language=en')
    r = requests.get(url)
    news = r.json()

    return news
