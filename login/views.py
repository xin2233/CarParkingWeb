from django.http import HttpResponse
from django.shortcuts import render, redirect
import hashlib

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from login import models
from login.forms import UserForm, RegisterForm

def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

# 测试反馈函数


@csrf_exempt  # 避免csrf ，在post表单中不需要添加｛%csrf_token%｝
def getex(request):
    # pass
    key = request.POST.get('key')
    bright = request.POST.get('bright')
    # key = request.GET.get('key')
    if key == '123': # 设备号对应响应的设备
        # 检测到了数据
        models.UserDetail.objects.filter(device_key=key).update(bright=bright)  # 更新数据进入数据库
        return HttpResponse('1')
    else:
        # 未检测到数据
        return HttpResponse('0')

def postex(request):  # 和前端按钮 形成控制，单机按钮 电机转动一定角度
    key = '123'
    car_status = models.UserDetail.objects.filter(device_key=key).values()[0]['car_status'] # 读取数据
    if car_status =="0":
        car_status = 1
    else:
        car_status = 0
    models.UserDetail.objects.filter(device_key=key).update(car_status=car_status)  # 更新数据进入数据库
    # return HttpResponse('2')  # 电机信号
    # pass
    return redirect("/index/")

def motor(request):  # 响应树莓派请求的函数，根据数据库内的值，反馈响应数据 2 未预约  3 已预约
    # key = request.GET.get('key')
    key = '123'
    car_status = models.UserDetail.objects.filter(device_key=key).values()[0]['car_status']  # 读取数据库中预约状态值 0 未预约 1 已预约
    if car_status == "0":
        return HttpResponse('2')  # 未预约
    else:
        return HttpResponse('3')  # 已预约


def index(request):
    # pass
    key = '123'
    bright = models.UserDetail.objects.filter(device_key=key).values()[0]['bright']
    car_status = models.UserDetail.objects.filter(device_key=key).values()[0]['car_status']
    return render(request, 'index.html',locals())


def login(request):
    if request.session.get('is_login', None):  # 如果已经登陆了就直接进入index
        return redirect('/index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password ==hash_code(password):    #哈希值和数据库内的值进行比较
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login.html', locals())

    login_form = UserForm()
    return render(request, 'login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)  #使用加密密码
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")
