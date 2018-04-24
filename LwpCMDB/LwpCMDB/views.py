#coding:utf-8
from django.shortcuts import render
from Admin.views import loginValid
from django.http import HttpResponseRedirect
import random
from django.db import connection

content = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz'

@loginValid
def index(request):
    return render(request, 'index.html',  locals())

def login(request):
    v_data = "".join(random.sample(content, 18))
    response = render(request, "login.html", locals())
    response.set_cookie("key", v_data)
    return response

def logout(request):
    c_phone = request.COOKIES.get("phone")
    s_phone = request.session.get("phone")
    if c_phone and s_phone:
        del request.COOKIES["phone"]
        del request.session["phone"]
    return HttpResponseRedirect("/login/")

def get_pageData(sql, page, num = 10):
    page = int(page)
    num = int(num)
    start_data = (page-1) * num
    page_data_sql = sql + " limit %s,%s" % (start_data, num)
    cur = connection.cursor()
    cur.execute(page_data_sql)
    page_data = cur.fetchall()
    desc = cur.description
    data_list = [
        dict(zip([d[0] for d in desc],row))
        for row in page_data ]
    page_total_sql = "select count(f.id) from (%s) as f" % sql
    cur.execute(page_total_sql)
    nums = cur.fetchone()[0]

    if nums % num == 0:
        page_total = nums / num
    else:
        page_total = nums / num + 1
    result = {
        "page_data": data_list,
        "page_range": range(page_total - 1, 0, -1)
    }
    return result




