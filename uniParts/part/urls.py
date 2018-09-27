from django.conf.urls import url
from .views import *

urlpatterns= [
    url(r'^partes/listar/$', parts_list, name='parts_list'),
    url(r'^partes/listar/(?P<tipo>[\w\-]+)/$', parts_list, name='parts_list'),
    url(r'^parte/new/$', parte_new, name='parte_new'),
    url(r'^parte/edit/(?P<pk>\d+)/$', parte_edit, name='parte_edit'),
    url(r'^parte/editar/(?P<pk>\d+)/$', editar, name='editar'),
    url(r'^validacao/new/(?P<pk>\d+)/$', validacao_new, name='validacao_new'),
    url(r'^encaminhado/(?P<pk>\d+)/$', encaminhar_parte, name='encaminhar_parte'),
    url(r'^exportToPdf/(?P<pk>\d+)/$', exportToPdf, name='exportToPdf'),
    url(r'^negado/(?P<pk>\d+)/$', negado, name='negado'),
    url(r'^$', parts_list, name='parts_list'),
    url(r'^lido/(?P<pk>\d+)/$', alerta_lido, name='alerta_lido'),
]
