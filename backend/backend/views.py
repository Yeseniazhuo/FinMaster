from django.shortcuts import render
from django.views import generic
from django.utils.safestring import mark_safe

from bokeh.plotting import figure
from bokeh.embed import components

from .utils import *

def plot_selected(selected_symbol):
    """
    Return the bokeh plot of selected symbol.
    """
    df = request_selected_symbol(selected_symbol)

    increasing=df.close > df.open
    decreasing=df.open > df.close
    w = 12 * 60 * 60 * 1000

    TOOLS = "pan, wheel_zoom, box_zoom, reset, save"
    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=820, plot_height=220)
    p.xaxis.major_label_orientation = 0

    p.grid.grid_line_alpha = 0.8

    p.segment(df.date, df.high, df.date, df.low, color="black")

    p.vbar(df.date[increasing], w, df.open[increasing], df.close[increasing],
        fill_color="#D5E1DD", line_color="black"
    )
    p.vbar(df.date[decreasing], w, df.open[decreasing], df.close[decreasing], 
        fill_color="#F2583E", line_color="black"
    )

    script, div = components(p)

    last_high = df.iloc[-1].high
    last_close = df.iloc[-1].close

    return script, div, last_high, last_close

def dashboard_news(keyword):
    news=request_selected_news(keyword)
    news_title_1=news['articles'][0]['title']
    news_content_1=news['articles'][0]['description']
    news_title_2=news['articles'][1]['title']
    news_content_2=news['articles'][1]['description']
    news_title_3=news['articles'][2]['title']
    news_content_3=news['articles'][2]['description']
    
    return news_title_1,news_title_2,news_title_3,news_content_1,news_content_2,news_content_3

def info_news(keyword):
    news=request_selected_news(keyword)
    news_title_1=news['articles'][0]['title']
    news_content_1=news['articles'][0]['description']
    news_title_2=news['articles'][1]['title']
    news_content_2=news['articles'][1]['description']
    news_title_3=news['articles'][2]['title']
    news_content_3=news['articles'][2]['description']
    news_title_4=news['articles'][3]['title']
    news_content_4=news['articles'][3]['description']
    news_title_5=news['articles'][4]['title']
    news_content_5=news['articles'][4]['description']
    news_title_6=news['articles'][5]['title']
    news_content_6=news['articles'][5]['description']

    return news_title_1,news_title_2,news_title_3,news_content_1,news_content_2,news_content_3,news_title_4,news_title_5,news_title_6,news_content_4,news_content_5,news_content_6

def dashboard(request):
    
    selected_symbol='AAPL'
    script, div, last_high, last_close=plot_selected(selected_symbol)

    keyword='AAPL AND stock'
    news_title_1,news_title_2,news_title_3,news_content_1,news_content_2,news_content_3=dashboard_news(keyword)

    context={
        'start_time':this_monday(),
        'this_month':this_month(),
        'selected_symbol':selected_symbol,
        'div':div,
        'script':script,
        'last_high':last_high,
        'last_close':last_close,
        'calendar':mark_safe(small_calendar()),
        'news_title_1':news_title_1,
        'news_content_1':news_content_1,
        'news_title_2':news_title_2,
        'news_content_2':news_content_2,
        'news_title_3':news_title_3,
        'news_content_3':news_content_3
    }

    return render(request,'Dashboard.html',context)

def calendar(request):
    context={}
    return render(request,'Calendar.html',context)

def info(request):
    keyword='AAPL AND stock'
    news_title_1,news_title_2,news_title_3,news_content_1,news_content_2,news_content_3,news_title_4,news_title_5,news_title_6,news_content_4,news_content_5,news_content_6=info_news(keyword)
    context={
        'news_title_1':news_title_1,
        'news_title_2':news_title_2,
        'news_title_3':news_title_3,
        'news_title_4':news_title_4,
        'news_title_5':news_title_5,
        'news_title_6':news_title_6,
        'news_content_1':news_content_1,
        'news_content_2':news_content_2,
        'news_content_3':news_content_3,
        'news_content_4':news_content_4,
        'news_content_5':news_content_5,
        'news_content_6':news_content_6
    }
    return render(request,'FinancialInfo.html',context)