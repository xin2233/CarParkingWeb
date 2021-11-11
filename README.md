# CarParkingWeb
this is my project for study only.

# 时间
2021/10/27：
by zjx;


# 项目使用说明： 
本工程是3年前编写，为个人学习物联网工程时，其中的服务器端项目，如今调试一下，进行开源。

（以下是我自己操作时，注册的账户。新的工程运行时需要自己重新注册 超级账户和login的账户）
账户：
超级管理员账户： admin ， 密码： admin
login账户： zjx    ，密码： zjx


1。安装 django，安装 mysql，下载工程
注意安装的django 版本和python 的版本需要对应。

2。创建超级账户： python manage.py createsuperuser

3.接下来是mysql的相关操作：
安装mysql部分--------省略；

create database auth_db;    ==>创建一个新的数据库文件夹auth_db
use auth_db；               ==>使用auth_db这个数据库
show tables；               ==>查看auth_db数据库中有哪些数据表

4.接下来是 数据库表的生成：
迁移数据库：python3 manage.py makemigrations   （生成迁移文件）
python3 manage.py migrate           （进行迁移）


本项目有一个设备信息，需要再mysql 中提前建立此设备信息 ：

（建议：运行工程，打开 http://127.0.0.1:8000/admin/ ，登录 超级账户，手动添加数据库的信息即可。参考以下：）

Device key:     123
Tem:            1
Hum:            1
Bright:         1
Car status:     1


运行程序：python3 manage.py runserver 0.0.0.0:8000