from backend.utils import *

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

def keywords_split(string):
    words = string.split(';')
    keywords = ' OR '.join(words)

    return keywords