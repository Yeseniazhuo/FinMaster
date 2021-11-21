from django.shortcuts import render
from django.views import generic
from django.utils.safestring import mark_safe

from bokeh.plotting import figure, ColumnDataSource
from bokeh.embed import components
from bokeh.models import BooleanFilter, CDSView, Select, Range1d, HoverTool
from bokeh.palettes import Category20
from bokeh.models.formatters import NumeralTickFormatter

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

def info_plot_1(selected_symbol):

    df = request_selected_symbol(selected_symbol)

    stock = ColumnDataSource(data=dict(date=[], open=[], close=[], high=[], low=[],index=[]))
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
    p = figure(plot_width=W_PLOT, plot_height=H_PLOT, tools=TOOLS, toolbar_location='right')

    inc = stock.data['close'] > stock.data['open']
    dec = stock.data['open'] > stock.data['close']
    view_inc = CDSView(source=stock, filters=[BooleanFilter(inc)])
    view_dec = CDSView(source=stock, filters=[BooleanFilter(dec)])

    # map dataframe indices to date strings and use as label overrides
    p.xaxis.major_label_overrides = {
        i+int(stock.data['index'][0]): date.strftime('%b-%d') for i, date in enumerate(pd.to_datetime(stock.data['date']))
    }
    p.xaxis.bounds = (stock.data['index'][0], stock.data['index'][-1])


    p.segment(x0='index', x1='index', y0='low', y1='high', color=RED, source=stock, view=view_inc)
    p.segment(x0='index', x1='index', y0='low', y1='high', color=GREEN, source=stock, view=view_dec)

    p.vbar(x='index', width=VBAR_WIDTH, top='open', bottom='close', fill_color=BLUE, line_color=BLUE,
           source=stock,view=view_inc, name="price")
    p.vbar(x='index', width=VBAR_WIDTH, top='open', bottom='close', fill_color=RED, line_color=RED,
           source=stock,view=view_dec, name="price")

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
    price_hover.formatters={"date": 'datetime'}

    script, div=components(p)
    return script, div

def info_plot_2(selected_symbol):

    

    return

#####################################Request####################################

############################dashboard############################
def dashboard(request):
    # render the picture and the news
    selected_symbol='SPY'
    script, div, last_high, last_close=plot_selected(selected_symbol)

    keyword='Stock'
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

    #create new issue
    if request.method == 'GET':
        if 'InputIssue' in request.GET:
            NewIssue = request.GET.get('InputIssue')
        if 'InputDue' in request.GET:
            NewDue = request.GET.get('InputDue')
        if 'InputTags' in request.GET:
            NewTags = request.GET.get('InputTags')

    return render(request,'Dashboard.html',context)

############################calendar############################
def calendar(request):
    context={
        'this_month':this_month(),
        'this_year':this_year(),
    }
    return render(request,'Calendar.html',context)

def info(request):
    keyword='AAPL AND stock'

    selected_symbol='AAPL'
    news_title_1,news_title_2,news_title_3,news_content_1,news_content_2,news_content_3,news_title_4,news_title_5,news_title_6,news_content_4,news_content_5,news_content_6=info_news(keyword)
    script_1,div_1=info_plot_1(selected_symbol)


    context={
        'div_1':div_1,
        'script_1':script_1,
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