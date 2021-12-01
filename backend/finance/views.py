from typing import Set
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import *
from .utils import *
from backend.utils import request_selected_symbol

# Create your views here.


def user_settings(request):

    instance = get_object_or_404(Settings, owner_id=request.user.id)
    if not instance:
        instance = Settings(owner=request.user)

    form = SettingsForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return redirect('/info/')

    return render(request, 'Settings.html', {'form': form})


def info(request):

    settings =get_object_or_404(Settings, owner=request.user)

    keyword = keywords_split(settings.keywords)
    news_title_1, news_title_2, news_title_3, news_content_1, news_content_2, news_content_3, news_title_4, news_title_5, news_title_6, news_content_4, news_content_5, news_content_6, news_url_1, news_url_2, news_url_3, news_url_4, news_url_5, news_url_6 = info_news(keyword)
    
    categoryData1, values1, last_high1, last_close1 = request_selected_symbol(settings.symbol1, settings.interval1)
    categoryData2, values2, last_high2, last_close2 = request_selected_symbol(settings.symbol2, settings.interval2)
    categoryData3, values3, last_high3, last_close3 = request_selected_symbol(settings.symbol3, settings.interval3)

    return render(request, 'FinancialInfo.html', locals())
