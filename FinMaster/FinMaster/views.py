from django.shortcuts import render
from django.template import loader,RequestContext
from django.http import HttpResponse

def render_html(request,template_path,context={}):
    #load template
    temp = loader.get_template(template_path)
    #define context, pass data to template
    context = RequestContext(request,context)
    #render
    response_html = temp.render(context)
    return HttpResponse(response_html)
