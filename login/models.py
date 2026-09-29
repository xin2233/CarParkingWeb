from django.conf import settings
from django.db import models

# Create your models here.


# 用户附加信息（账号本体使用 Django 内置 auth.User）
class Profile(models.Model):
    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sex = models.CharField(max_length=32, choices=gender, default='male')
    # 旧版自定义用户表（login_user）的 SHA-256 密码，登录成功时自动升级为 Django 哈希后清空
    legacy_password = models.CharField(max_length=256, blank=True, default='')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'


# 设备信息
class UserDetail(models.Model):
    device_key = models.CharField(max_length=150, default=1)
    tem = models.CharField(max_length=150)
    hum = models.CharField(max_length=150)
    bright = models.CharField(max_length=150)
    car_status = models.CharField(max_length=150)  # 0 未预约, 1 已预约

    class Meta:
        verbose_name = '设备信息'
        verbose_name_plural = verbose_name
