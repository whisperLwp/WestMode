#coding:utf-8
from django.conf.urls import include, url
from django.contrib import admin
from views import *

urlpatterns = [
    url(r'^$', user_list),
    url(r'^phonevalid/$',phoneValid ),
    url(r'^login/$', login),
    url(r'^logout', logout),
    url(r'^uvalid',uvalid),
    url(r'^user', user),
    url(r'^uchange', username_change),
    url(r'^echange', eml_change),
    url(r'^pchange', pwd_change),

]
