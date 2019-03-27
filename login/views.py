import hashlib

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from login import models
# Create your views here.
import json

#实现登录功能
@csrf_exempt
def login(request):
    if request.content_type != 'application/json':
        return getWrongRespoonse()
    my_dict = getDict(request)
    if request.method == "POST":
        if 'username' not in my_dict.keys() or 'password' not in my_dict.keys():
            return getWrongRespoonse()
        username = my_dict['username']
        password = my_dict['password']
        if username and password:
            username = username.strip()
            try:
                user = models.User.objects.get(name=username)
                if user.password == hashCode(password):
                    # 验证当前请求和以前以及以后的请求是否为同一用户
                    return JsonResponse({'name': username, 'password': password})
                else:
                    message = "密码错误!"
            except:
                message = "用户名不存在!"
            return JsonResponse({'message': message})
    return getWrongRespoonse()


@csrf_exempt
def logout(request):
    pass

#实现注册功能
@csrf_exempt
def register(request):
    my_dict = getDict(request)
    if request.method == "POST":
        message_tips = "请检查你输入的内容！"
        if my_dict['type'] == 'register':
            username = my_dict['username']
            password1 = my_dict['password1']
            password2 = my_dict['password2']
            email = my_dict['email']
            sex = my_dict['sex']
            if password1 != password2:
                message_tips = "两次输入的密码不一致！"
                return JsonResponse({'message_tips': message_tips})
            else:
                same_name_user = models.User.objects.filter(name=username)
                # django中的filter方法是从数据库取得匹配的结果，返回一个对象表，如果记录不存在的话
                # 返回【】

                if same_name_user:
                    message_tips = "用户已经存在，请重新选择用户名！"
                    return JsonResponse({'message_tips': message_tips})
                same_email_user = models.User.objects.filter(email=email)

                if same_email_user:
                    message_tips = "该邮箱地址已被注册，请使用别的邮箱！"
                    return JsonResponse({'message_tips': message_tips})

                createUser(username, password1, email, sex)
                message_tips = "注册成功！"
                return JsonResponse({'message_tips': message_tips})

#向数据库创建一个新的用户
def createUser(username, password, email, sex):
    '''

    :param username:
    :param password:
    :param email:
    :param sex:
    :return: /
    '''
    new_user = models.User.objects.create()
    new_user.name = username
    new_user.password = hashCode(password)
    new_user.email = email
    new_user.sex = sex
    new_user.save()

 #提取json表单
def getDict(request):
    message = request.body.decode()
    my_json = json.loads(message)
    my_dict = dict(my_json)
    return my_dict
#错误类型提示
def getWrongRespoonse(num):
    status=[
        '请求类型不是Json!',
        '请求类型不是POST!'
    ]
    message=status[num]
    wrongType=[-1,-2]
    return JsonResponse({"status": wrongType[num], "message": message})

#错误类型提示
def getWronglogin(num):
    status=[
        '密码错误',
        ''
    ]
#对输入的数据进行hash以增加其安全性
def hashCode(s,salt='login_1_login'):
    h=hashlib.sha256()
    s+=salt
    h.update(s.encode())
    return h.hexdigest()
