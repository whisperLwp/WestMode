#coding:utf-8
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from models import Equipment
from LwpCMDB.views import get_pageData
import paramiko

def eq_list(request):
    if request.method == "GET":
        requestData = request.GET
        page = requestData.get("page")
        num = requestData.get("num")
        sql = "select * from Equipment_equipment"
        if page and num:
            result = get_pageData(sql = sql,page = page,num = num)
        elif page :
            result = get_pageData(sql=sql, page=page)
        else:
            result = {
                "page_data": "",
                "page_range": ""
            }
    else:
        result = {
            "page_data": "",
            "page_range": ""
        }
    return JsonResponse(result)

def eq_list_page(request):
    eq_List = Equipment.objects.all()
    return render(request,"equipmentList.html",locals())

def eq_add(request):
    result = {"state":"error", "data":""}
    if request.method == "POST":
        data = request.POST
        ip = data.get("ip")
        port = data.get("port")
        user = data.get("username")
        password = data.get("password")
        if ip and port and user and password:
            eq = Equipment()
            eq.IP = ip
            eq.User = user
            eq.Password = password
            try:
                trans = paramiko.Transport(ip, port)
                trans.connect(username=user, password=password)
                sftp = paramiko.SFTPClient.from_transport(trans)
                ssh = paramiko.SSHClient()
                ssh._transport = trans
                stdin,stdout,stderr = ssh.exec_command("mkdir CMDBClient")
                sftp.put("sftpDir/getData.py", "/root/CMDBClient/getData.py")
                sftp.put("sftpDir/sendData.py", "/root/CMDBClient/sendData.py")
                sftp.put("sftpDir/main.py", "/root/CMDBClient/main.py")
                stdin,stdout,stderr = ssh.exec_command("python /root/CMDBClient/main.py")
                trans.close()
                result["state"] = "success"
                result["data"] = "操作成功！"
                eq.Statue = "True"
            except Exception as e:
                eq.Statue = "False"
                result["data"] = "远程连接错误：%s" % e
            finally:
                eq.save()
        else:
            result["data"] = "IP、port、user、password不能为空，请检查"
    else:
        result["data"] = "请求错误，请刷新重试"
    return JsonResponse(result)

def eq_drop(request):
    pass

def eq_alter(request):
    pass

@csrf_exempt
def eq_save(request):
    ip = request.META["REMOTE_ADDR"]
    if request.method == "POST":
        data = request.POST
        hostname = data.get("get_hostname")
        system = data.get("get_system")
        mac = data.get("get_mac")

        equpment = Equipment.objects.get(IP = ip)
        equpment.hostname = hostname
        equpment.System = system
        equpment.Mac = mac
        equpment.save()

    return JsonResponse({"state":"this only a test"})

terminal_dict = {}

def shell(request):
    if request.method == "GET":
        id = request.GET["id"]
        if id:
            equipment = Equipment.objects.get(id = int(id))
            ip = equipment.IP
            username = equipment.User
            password = equipment.Password
            if ip and username and password:
                try:
                    result = {"status":"success","ip":ip,}
                    trans = paramiko.Transport(sock = (ip,22))
                    trans.connect(
                        username = username,
                        password = password
                    )
                    ssh = paramiko.SSHClient()
                    ssh._transport = trans
                    terminal = ssh.invoke_shell()
                    terminal.settimeout(2)
                    terminal.send("\n")
                    login_data = ""
                    while True:
                        try:
                            recv = terminal.recv(9999)
                            if recv:
                                login_data += recv
                            else:
                                continue
                        except:
                            break
                    result["data"] = login_data.replace("\r\n","<br>")
                    terminal_dict[ip] = terminal
                    response = render(request, "shell.html", locals())
                    response.set_cookie("ip",ip)
                    return response
                except Exception as e:
                    print(e)
                    return HttpResponseRedirect("/eq/")
def command(request):
    result = {"data":""}
    ip = request.COOKIES.get("ip")
    if ip:
        if request.method == "GET":
            cmd = request.GET.get("command")
            if cmd:
                if cmd == "clear":
                    return JsonResponse(result)
                else:
                    terminal = terminal_dict[ip]
                    terminal.send(cmd+"\n")
                    #login_data = ""
                    while True:
                        try:
                            recv = terminal.recv(9999)
                            if recv:
                                line_list = recv.split("\r\n")
                                result_list= []
                                for line in line_list:
                                    l = line.replace(u"\u001B","").replace("[01;34m","").replace("[0m","").replace("[01;32m","")
                                    result_list.append(l)
                                login_data = "<br>".join(result_list)

                            else:
                                continue
                        except:
                            break
                result["data"] = login_data
                return JsonResponse(result)
            else:
                return HttpResponseRedirect("/eq/")
        else:
            return HttpResponseRedirect("/eq/")
    else:
        return HttpResponseRedirect("/eq/")


import random

def add_eq(request):
    for i in range(100):
        e = Equipment()
        e.hostname = "localhost_%s"%i
        e.IP = "192.168.1.%s"%(i+2)
        e.System = random.choice(["win7_32","win7_64","centos.6_32","centos.7",])
        e.Statue = random.choice(["True","False"])
        e.Mac = random.choice(["00:0c:29:92:85:4e","00:0c:29:5b:2a:a1"])
        e.user = "root"
        e.Password = "123"
        e.save()
    return JsonResponse({"statue":"ahh"})