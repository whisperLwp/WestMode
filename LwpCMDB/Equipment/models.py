#coding:utf-8
from django.db import models

class Equipment(models.Model):
    hostname = models.CharField(max_length = 32, verbose_name = "服务器名称")
    System = models.CharField(max_length = 32, verbose_name = "服务器系统")
    Mac = models.CharField(max_length = 32, verbose_name = "mac地址")
    IP = models.CharField(max_length = 32, verbose_name = "ip地址")
    Statue = models.CharField(max_length = 32, verbose_name = "服务器状态")
    User = models.CharField(max_length = 32, verbose_name = "用户名")
    Password = models.CharField(max_length = 32, verbose_name = "密码")
