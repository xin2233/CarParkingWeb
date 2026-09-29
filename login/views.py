import hashlib

from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt

from login import models
from login.forms import UserForm, RegisterForm

def _device_key():
    return settings.DEVICE_KEY


def _device_token():
    return settings.DEVICE_TOKEN


def _legacy_hash(s, salt='mysite'):  # 旧版自定义用户表的密码哈希算法，仅用于登录时校验旧密码
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def _device_authenticated(request):
    """设备接口鉴权：优先从 X-Device-Token 请求头取 token，兼容 POST/GET 的 token 字段"""
    token = request.headers.get('X-Device-Token') or request.POST.get('token') or request.GET.get('token')
    return token == _device_token()


@csrf_exempt  # 设备端无浏览器会话，使用 token 鉴权替代 CSRF
def getex(request):
    if not _device_authenticated(request):
        return HttpResponse('0')
    key = request.POST.get('key')
    bright = request.POST.get('bright')
    if key == _device_key():  # 设备号对应响应的设备
        # 检测到了数据
        models.UserDetail.objects.filter(device_key=key).update(bright=bright)  # 更新数据进入数据库
        return HttpResponse('1')
    else:
        # 未检测到数据
        return HttpResponse('0')


@login_required
def postex(request):  # 和前端按钮 形成控制，单机按钮 电机转动一定角度
    key = _device_key()
    detail = models.UserDetail.objects.filter(device_key=key).first()
    if detail is None:
        return redirect("/index/")
    car_status = detail.car_status  # 读取数据
    if car_status == "0":
        car_status = 1
    else:
        car_status = 0
    models.UserDetail.objects.filter(device_key=key).update(car_status=car_status)  # 更新数据进入数据库
    return redirect("/index/")


def motor(request):  # 响应树莓派请求的函数，根据数据库内的值，反馈响应数据 2 未预约  3 已预约
    if not _device_authenticated(request):
        return HttpResponse('0')
    key = _device_key()
    detail = models.UserDetail.objects.filter(device_key=key).first()
    if detail is None:
        return HttpResponse('0')
    car_status = detail.car_status  # 读取数据库中预约状态值 0 未预约 1 已预约
    if car_status == "0":
        return HttpResponse('2')  # 未预约
    else:
        return HttpResponse('3')  # 已预约


@login_required
def index(request):
    key = _device_key()
    detail = models.UserDetail.objects.filter(device_key=key).first()
    if detail is None:
        bright = None
        car_status = None
    else:
        bright = detail.bright
        car_status = detail.car_status
    return render(request, 'index.html', {'bright': bright, 'car_status': car_status})


def _legacy_password_login(username, password):
    """旧账号（login_user 迁移而来）登录：legacy_password 中存有 SHA-256 哈希，
    校验通过后升级为 Django 哈希并清空。返回升级后的 User 或 None。"""
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None
    try:
        profile = user.profile
    except models.Profile.DoesNotExist:
        return None
    if profile.legacy_password and profile.legacy_password == _legacy_hash(password):
        user.set_password(password)  # 升级为 Django 哈希
        user.save()
        profile.legacy_password = ''
        profile.save()
        return user
    return None


def login(request):
    if request.user.is_authenticated:  # 如果已经登陆了就直接进入index
        return redirect('/index/')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is None:
                user = _legacy_password_login(username, password)  # 兼容旧账号首次登录
            if user is not None:
                auth_login(request, user)
                return redirect('/index/')
            else:
                message = "用户名或密码不正确！"
        return render(request, 'login.html', {'login_form': login_form, 'message': message})

    login_form = UserForm()
    return render(request, 'login.html', {'login_form': login_form})


def register(request):
    if request.user.is_authenticated:
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
                return render(request, 'register.html', {'register_form': register_form, 'message': message})
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                message = '用户名或邮箱已被注册，请重新填写！'
                return render(request, 'register.html', {'register_form': register_form, 'message': message})

                # 当一切都OK的情况下，创建新用户（并发场景由数据库唯一约束兜底）
            try:
                new_user = User.objects.create_user(
                    username=username, password=password1, email=email)
            except IntegrityError:
                message = '用户名或邮箱已被注册，请重新填写！'
                return render(request, 'register.html', {'register_form': register_form, 'message': message})
            models.Profile.objects.create(user=new_user, sex=sex)
            return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'register.html', {'register_form': register_form})


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect("/index/")
