# 1. 更新 Django 3.2 解决 DEFAULT_AUTO_FIELD warnings

https://blog.csdn.net/sunjl_a/article/details/116482203

# 2. 解决Django项目数据库无法迁移问题

找到自己的虚拟环境，以下是我自己的环境路径
  D:\xunihuanjing\venv\Lib\site-packages\django\contrib\admin\migrations
然后删除里面的迁移记录。

# 3. No changes detected报错解决方案
一、问题描述
　　执行python3 manage.py makemigrations提示：No changes detected

二、解决方案
第一种解决方案：需要在makemigrations后面加应用名称，即python3 manage.py makemigrations App，App是我的应用名称
第二种解决方案：执行python3 manage.py makemigrations --empty App

# 4. 【解决方案】Django中数据迁移错误提示“No changes detected”的解决

https://blog.csdn.net/chichu261/article/details/82868597

# 5. 'staticfiles' is not a registered tag library.

主要是因为：staticfiles is now deprecated and you have to load it as {% load static %} instead of old way {% load static from staticfiles %}

Release notes for 3.0 version

https://blog.csdn.net/LI4836/article/details/103871590?spm=1001.2101.3001.6650.2&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-2.no_search_link&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-2.no_search_link


# 6 . Table 'MyDjango.django_admin_log' doesn't exist

    使用django_damin后台时,数据库没有自动生成django_admin_log,需要单独迁移文件admin应用

python manage.py makemigrations admin
python manage.py migrate admin
    报错如下：

    err.raise_mysql_exception(self._data)
  File "/usr/local/python36/lib/python3.6/site-packages/pymysql/err.py", line 109, in raise_mysql_exception
    raise errorclass(errno, errval)
django.db.utils.ProgrammingError: (1146, "Table 'polls.django_admin_log' doesn't exist")
[18/Sep/2020 18:42:35] "GET /admin/ HTTP/1.1" 500 350858
    迁移admin应用

[root@opsys-vm15-253 mysite]# python3 manage.py makemigrations admin
Migrations for 'admin':
  /usr/local/python36/lib/python3.6/site-packages/django/contrib/admin/migrations/0001_initial.py
    - Create model LogEntry
[root@opsys-vm15-253 mysite]# python3 manage.py migrate admin
Operations to perform:
  Apply all migrations: admin
Running migrations:
  Applying admin.0001_initial... OK
[root@opsys-vm15-253 mysite]# python3 manage.py runserver 0.0.0.0:8000
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
September 18, 2020 - 19:18:23
Django version 2.2.3, using settings 'mysite.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.

https://www.qedev.com/python/316629.html

end