from django.conf.urls import url
from .views import *
from . import views
from django.contrib import admin

urlpatterns= [
    url(r'^partes/listar/$', parts_list, name='parts_list'),
    url(r'^partes/listar/(?P<tipo>[\w\-]+)/$', parts_list, name='parts_list'),
    url(r'^parte/new/$', parte_new, name='parte_new'),
    url(r'^validacao/new/(?P<pk>\d+)/$', validacao_new, name='validacao_new'),
    url(r'^$', parts_list, name='parts_list'),
]
