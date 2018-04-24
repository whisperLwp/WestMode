#coding:utf-8
from django.conf.urls import include, url
from django.contrib import admin
from views import *

urlpatterns = [
    url(r'^eq_add/', eq_add),
    url(r'^eqList/', eq_list_page),
    url(r'^$', eq_list_page),
    url(r'eq_save', eq_save),
    url(r'eq_list', eq_list),
    url(r'ade', add_eq),
    url(r'shell', shell),
    url(r'cmd', command),
]
