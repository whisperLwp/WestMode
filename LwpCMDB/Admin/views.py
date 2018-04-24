#coding:utf-8
from django.shortcuts import render
from forms import Register
from models import User
from django.http import JsonResponse,HttpResponseRedirect
import hashlib
from PIL import Image

def phoneValid(request):
    result = {"state":"error", "data": ""}
    if request.method == "GET":
        phoneNum = request.GET.get("phone_num")
        if phoneNum:
            try:
                u = User.objects.get(phone=phoneNum)
            except:
                result["state"] = "success"
                result["data"] = "该电话号码可用"
            else:
                result["data"] = "该电话号码不可用"
        else:
            result["data"] = ""
    else:
        result["data"] = "请重新输入"
    return JsonResponse(result)

def getmd5(passwd):
    md5 = hashlib.md5()
    md5.update(passwd)
    return md5.hexdigest()

def loginValid(fun):
    def inner(request,*args, **kwargs):
        cookie = request.COOKIES
        cPhone = cookie.get("phone")
        sPhone = request.session.get("phone")
        if cPhone and cPhone == sPhone:
            return fun(request,*args, **kwargs)
        else:
            return HttpResponseRedirect("/login")
    return inner

def login(request):
    result = {"state": "error", "data": ""}
    if request.method == "POST":
        userdata = request.POST
        username = userdata.get("phone")
        password = userdata.get("password")
        vdata = userdata.get("remember")
        cookiedata = request.COOKIES.get("key")
        if vdata == cookiedata:
            try:
                u = User.objects.get(phone=username)
            except:
                result["data"] = "请输入正确的用户名"
                return JsonResponse(result)
            else:
                postPassword = getmd5(password)
                if postPassword == u.password:
                    result["state"] = "success"
                    response = JsonResponse(result)
                    response.set_cookie("phone", u.phone)
                    request.session["phone"] = u.phone
                    request.session["user_id"] = u.id
                    return response
                else:
                    result["data"] = "密码错误"
                    return JsonResponse(result)
        else:
            result["data"] = "请刷新重试"
    return JsonResponse(result)

def uvalid(request):
    result = {"state":"error", "data":""}
    if request.method == "GET":
        try:
            phone = request.GET.get("phone")
            u = User.objects.get(phone = phone)
        except KeyError as e:
            result["data"] = "手机号不可为空"
        except:
            result["data"] = "改手机号不存在"
        else:
            result["state"] = "success"
            result["error"] = "ok"
    else:
        result["data"] = "请求错误"
    return JsonResponse(result)

def user_list(request):
    register = Register
    if request.method == "POST":
        data = request.POST
        img = request.FILES
        #获取前端返回内容
        username = data.get("username")
        password = data.get("password")
        phone = data.get("phone")
        email = data.get("email")
        photo = img.get("photo")
        #保存头像图片到本地
        name = "static/img" + photo.name
        img = Image.open(photo)
        img.save(name)
        #将数据保存到数据库
        user = User()
        user.username = username
        user.password = getmd5(password)
        user.phone = phone
        user.email = email
        user.photo = "img/"+photo.name
        user.save()
    return render(request, "userList.html", locals())

def user(request):
    if request.method == "GET":
        try:
            phone = request.COOKIES.get("phone")
            user = User.objects.get(phone = phone)
        except:
            HttpResponseRedirect("/login/")
        else:
            name = user.username
            password = user.password
            email = user.email
            return render(request, "userm.html", locals())
    else:
        return HttpResponseRedirect("/login/")
def username_change(request):
    result = {"state":"error","data":""}
    if request.method == "GET":
        phone = request.COOKIES.get("phone")
        user = User.objects.get(phone = phone)
        name = request.GET.get("userN")
        if name:
            user.username = name
            result["state"] = "success"
            result["data"] = "用户名修改成功"
            user.save()
        else:
            result["data"] = "用户名不能为空"
    else:
        result["data"] = "请求错误请刷新重试"
    return JsonResponse(result)
def eml_change(request):
    result = {"state": "error", "data": ""}
    if request.method == "GET":
        phone = request.COOKIES.get("phone")
        user = User.objects.get(phone=phone)
        eml = request.GET.get("eml")
        if eml:
            user.email = eml
            result["state"] = "success"
            result["data"] = "Email地址修改成功"
            user.save()
        else:
            result["data"] = "Email地址不能为空"
    else:
        result["data"] = "请求错误请刷新重试"
    return JsonResponse(result)
def pwd_change(request):
    result = {"state": "error","data": ""}
    if request.method == "POST":
        phone = request.COOKIES.get("phone")
        user = User.objects.get(phone=phone)
        oldpwd = request.POST.get("oldPWD")
        oldpwd_md5 = getmd5(oldpwd)
        password = user.password
        if oldpwd_md5 == password:
            newpwd1 = request.POST.get("newPWD")
            newpwd2 = request.POST.get("newPWD2")
            if newpwd1 and newpwd2:
                if newpwd1 == newpwd2:
                    newpwd = getmd5(newpwd1)
                    user.password = newpwd
                    user.save()
                    result["state"] = "success"
                    result["data"] = "修改密码成功！"
                else:
                    result["data"] = "两次密码输入不一致！"
            else:
                result["data"] = "新密码不能为空！"
        else:
            result["data"] = "请输入正确的原密码！"
    else:
        result["data"] = "请求错误，请重试！"
    return JsonResponse(result)

def user_alter(request):
    pass

def user_drop(request):
    pass

def logout(request):
    pass

def register(request):
    pass

