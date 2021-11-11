# 1. django版本和python版本的对应

Django version		python versions
1.8					2.7,3.2,3.3,3.4,3.5
1.9,1.10			2.7,3.4,3.5
1.11				2.7,3.4,3.5,3.6
2.0					3.4,3.5,3.6
2.1					3.5,3.6,3.7
3.2                 3.9

//////////////////////////
/* 本工程采用 diango 3.0 */
//////////////////////////

步骤：



# 2. 创建一个工程，并运行
 https://www.runoob.com/django/django-first-app.html


# 3. Django操作MySql详细教程

https://blog.csdn.net/weixin_43499626/article/details/84351572

# 4. django创建超级用户
一、首先创建一个新用户，用来登录Django管理网站，进入manage.py目录下，使用如下命令来进行创建：
>>python manage.py createsuperuser

二、接下来输入用户名称：
>>Username(leave bkank to use 'administrator'): root

三、然后是输入邮箱（QQemail等都可以）：
>>Email address：（输入你的邮箱账号）

四、输入密码（输入密码时不会显示出来，并且长度必须超过八位才行）：
>>Password：********
>>Password(again)：********

当两次密码输入相同且超过八位的时候，就会提示创建超级用户成功：
>>Superuser created successfully.

再次运行你的服务，输入账号和密码就可以成功登陆了：
>>python manage.py runserver
