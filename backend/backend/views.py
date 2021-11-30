from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.utils.safestring import mark_safe
from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

from bokeh.plotting import figure, ColumnDataSource
from bokeh.embed import components
from bokeh.models import BooleanFilter, CDSView, Select, Range1d, HoverTool
from bokeh.palettes import Category20
from bokeh.models.formatters import NumeralTickFormatter

from datetime import datetime
import base64
from io import BytesIO

from .utils import *
from task.models import *


def plot_dashboard(selected_symbol):
    """
    Return the bokeh plot of selected symbol.
    """
    df = request_selected_symbol(selected_symbol)

    increasing = df.close > df.open
    decreasing = df.open > df.close
    w = 12 * 60 * 60 * 1000

    TOOLS = "pan, wheel_zoom, box_zoom, reset, save"
    p = figure(x_axis_type="datetime", tools=TOOLS,
               plot_width=820, plot_height=220)
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


def info_news(keyword):
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
    news_title_4 = news['articles'][3]['title']
    news_content_4 = news['articles'][3]['description']
    news_url_4 = news['articles'][3]['url']
    news_title_5 = news['articles'][4]['title']
    news_content_5 = news['articles'][4]['description']
    news_url_5 = news['articles'][4]['url']
    news_title_6 = news['articles'][5]['title']
    news_content_6 = news['articles'][5]['description']
    news_url_6 = news['articles'][5]['url']

    return news_title_1, news_title_2, news_title_3, news_content_1, news_content_2, news_content_3, news_title_4, news_title_5, news_title_6, news_content_4, news_content_5, news_content_6, news_url_1, news_url_2, news_url_3, news_url_4, news_url_5, news_url_6


def info_plot_1(selected_symbol):

    df = request_selected_symbol(selected_symbol)

    stock = ColumnDataSource(
        data=dict(date=[], open=[], close=[], high=[], low=[], index=[]))
    stock.data = stock.from_df(df)

    # Define constants
    W_PLOT = 850
    H_PLOT = 280
    TOOLS = 'pan,wheel_zoom,hover,reset'

    VBAR_WIDTH = 0.2
    RED = Category20[7][6]
    GREEN = Category20[5][4]

    BLUE = Category20[3][0]
    BLUE_LIGHT = Category20[3][1]

    ORANGE = Category20[3][2]
    PURPLE = Category20[9][8]
    BROWN = Category20[11][10]
    p = figure(x_axis_type="datetime", plot_width=W_PLOT, plot_height=H_PLOT,
               tools=TOOLS, toolbar_location='right')

    inc = stock.data['close'] > stock.data['open']
    dec = stock.data['open'] > stock.data['close']
    view_inc = CDSView(source=stock, filters=[BooleanFilter(inc)])
    view_dec = CDSView(source=stock, filters=[BooleanFilter(dec)])

    # map dataframe indices to date strings and use as label overrides
    p.xaxis.major_label_overrides = {
        i+int(stock.data['index'][0]): date.strftime('%b-%d') for i, date in enumerate(pd.to_datetime(stock.data['date']))
    }
    p.xaxis.bounds = (stock.data['index'][0], stock.data['index'][-1])

    p.segment(x0='index', x1='index', y0='low', y1='high',
              color=RED, source=stock, view=view_inc)
    p.segment(x0='index', x1='index', y0='low', y1='high',
              color=GREEN, source=stock, view=view_dec)

    p.vbar(x='index', width=VBAR_WIDTH, top='open', bottom='close', fill_color=BLUE, line_color=BLUE,
           source=stock, view=view_inc, name="price")
    p.vbar(x='index', width=VBAR_WIDTH, top='open', bottom='close', fill_color=RED, line_color=RED,
           source=stock, view=view_dec, name="price")

    p.legend.location = "top_left"
    p.legend.border_line_alpha = 0
    p.legend.background_fill_alpha = 0
    p.legend.click_policy = "mute"

    p.yaxis.formatter = NumeralTickFormatter(format='$ 0,0[.]000')
    p.x_range.range_padding = 0.05
    p.xaxis.ticker.desired_num_ticks = 40
    p.xaxis.major_label_orientation = 3.14/4

    # Select specific tool for the plot
    price_hover = p.select(dict(type=HoverTool))

    # Choose, which glyphs are active by glyph name
    price_hover.names = ["price"]
    # Creating tooltips
    price_hover.tooltips = [("Datetime", "@date{%Y-%m-%d}"),
                            ("Open", "@open{$0,0.00}"),
                            ("Close", "@close{$0,0.00}"),
                            ("Volume", "@volume{($ 0.00 a)}")]
    price_hover.formatters = {"date": 'datetime'}

    script, div = components(p)
    return script, div


def info_plot_2(selected_symbol):
    """
    Plot the SMA comparsion
    """
    # merge SMA togethor
    SMA_5 = get_n_days_SMA_data(selected_symbol, 5)
    SMA_10 = get_n_days_SMA_data(selected_symbol, 10)
    SMA_df = pd.merge(SMA_5, SMA_10, on='date')
    quarter_ago = datetime.now() + timedelta(days=-90)
    SMA_df = SMA_df.loc[SMA_df.date >= quarter_ago].reset_index(drop=True)

    # Define constants
    W_PLOT = 850
    H_PLOT = 280
    TOOLS = 'pan,wheel_zoom,hover,reset'

    # plot
    p = figure(x_axis_type="datetime", plot_width=W_PLOT,
               plot_height=H_PLOT, tools=TOOLS, toolbar_location='right')
    p.line(SMA_df['date'], SMA_df['SMA_5'],
           legend_label='5 days SMA', line_color="tomato")
    p.line(SMA_df['date'], SMA_df['SMA_10'],
           legend_label='10 days SMA', line_color="blue")

    # set legend
    p.legend.location = "top_left"
    p.legend.border_line_alpha = 0
    p.legend.background_fill_alpha = 0
    p.legend.click_policy = "mute"

    # set x_axis y_axis
    p.yaxis.formatter = NumeralTickFormatter(format='$ 0,0[.]000')
    p.x_range.range_padding = 0.1
    p.xaxis.ticker.desired_num_ticks = 40
    p.xaxis.major_label_orientation = 3.14/4

    # delete grid
    p.xgrid.visible = True
    p.ygrid.visible = True

    script, div = components(p)
    return script, div


def info_plot_3(selected_symbol):
    # Merge index and stock
    stock = request_selected_symbol(selected_symbol)
    stock['close'] = stock['close'].pct_change(1)
    stock = stock.rename(columns={'close': 'stock_close'})
    stock = stock[['date', 'stock_close']]
    index = request_selected_symbol('SPY')
    index['close'] = index['close'].pct_change(1)
    index = index.rename(columns={'close': 'index_close'})
    index = index[['date', 'index_close']]
    index['index_close'] = index['index_close']  # divide by 100 for comparsion
    Compar = pd.merge(stock, index, on='date')
    month_ago = datetime.now() + timedelta(days=-30)
    Compar = Compar.loc[Compar.date >= month_ago].reset_index(drop=True)

    # Define constants
    W_PLOT = 850
    H_PLOT = 280
    TOOLS = 'pan,wheel_zoom,hover,reset'

    # plot
    p = figure(x_axis_type="datetime", plot_width=W_PLOT,
               plot_height=H_PLOT, tools=TOOLS, toolbar_location='right')
    p.line(Compar['date'], Compar['stock_close'],
           legend_label=selected_symbol+' Daily Return', line_color="tomato")
    p.line(Compar['date'], Compar['index_close'],
           legend_label='S&P 500'+' Daily Return', line_color="blue")

    # set legend
    p.legend.location = "top_left"
    p.legend.border_line_alpha = 0
    p.legend.background_fill_alpha = 0
    p.legend.click_policy = "mute"

    # set x_axis y_axis
    p.yaxis.formatter = NumeralTickFormatter(format=' 0,0[.]000')
    p.x_range.range_padding = 0.1
    p.xaxis.ticker.desired_num_ticks = 40
    p.xaxis.major_label_orientation = 3.14/4

    # delete grid
    p.xgrid.visible = True
    p.ygrid.visible = True

    script, div = components(p)
    return script, div


def progress_count(request):
    unfinished_tasks = Task.objects.filter(owner=request.user, due__lte=datetime.today().replace(hour=23,minute=59,second=59), due__gte=datetime.today().replace(hour=23,minute=59,second=59) + timedelta(days=-7), complete_status=False)
    finished_tasks = Task.objects.filter(owner=request.user, due__lte=datetime.today().replace(hour=23,minute=59,second=59), due__gte=datetime.today().replace(hour=23,minute=59,second=59) + timedelta(days=-7),  complete_status=True)
    unfinished = len(unfinished_tasks)
    finished = len(finished_tasks)
    return unfinished, finished


def dashboard(request, task_id=None):

    unfinished, finished = progress_count(request)
    #print(unfinished, finished)
    #print(request.user)

    selected_symbol = 'SPY'
    script, div, last_high, last_close = plot_dashboard(selected_symbol)

    keyword = 'stock'
    news_title_1, news_title_2, news_title_3, news_content_1, news_content_2, news_content_3, news_url_1, news_url_2, news_url_3 = dashboard_news(
        keyword)

    start_time = datetime.today().strftime('%Y-%m-%d')
    month = this_month()

    today = datetime.today().day

    Delaytask = Task.objects.filter(owner=request.user, due__lte=datetime.now(), complete_status=False)
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

    tasks = Task.objects.filter(owner=request.user, due__lte=datetime.now()+timedelta(days=1), complete_status=False).order_by('due').reverse()
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


def info(request):

    keyword = 'AAPL AND stock'

    selected_symbol = 'AAPL'
    news_title_1, news_title_2, news_title_3, news_content_1, news_content_2, news_content_3, news_title_4, news_title_5, news_title_6, news_content_4, news_content_5, news_content_6, news_url_1, news_url_2, news_url_3, news_url_4, news_url_5, news_url_6 = info_news(
        keyword)
    script_1, div_1 = info_plot_1(selected_symbol)
    script_2, div_2 = info_plot_2(selected_symbol)
    script_3, div_3 = info_plot_3(selected_symbol)

    return render(request, 'FinancialInfo.html', locals())
