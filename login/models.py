from django.db import models

# Create your models here.


# 用户信息
class User(models.Model):
    # 用户表

    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


# 用户的详情信息
class UserDetail(models.Model):
    # username = models.CharField(max_length=150)
    device_key = models.CharField(max_length=150, default=1)
    tem = models.CharField(max_length=150)
    hum = models.CharField(max_length=150)
    bright = models.CharField(max_length=150)
    car_status = models.CharField(max_length=150)  # 0 不在， 1 在


    class Meta:
        verbose_name = '设备信息'
        verbose_name_plural = verbose_name
