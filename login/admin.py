from django.contrib import admin

# Register your models here.

from django.contrib import admin
from . import models

admin.site.site_header=u"智能停车场管理界面"
admin.site.site_title = u"个人管理界面"

admin.site.register(models.User)
admin.site.register(models.UserDetail)
