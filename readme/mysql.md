# 1.下载MySQL，步骤①==>步骤②

# 2.下载后，解压到除系统盘(C盘)之外的其他盘中

# 3.解压后在bin目录所在级新建data目录(后续初始化、新建数据库、授权用户权限等)

# 4.服务端初始化操作(mysqld)

Windows标志+r，输入cmd，打开命令提示符工具。然后在命令提示符工具中输入MySQL所安装的盘符(我的是D：)，Enter回车。进入D盘后，在安装文件夹中找到bin目录，在该目录中找到可执行文件mysql.exe，将改文件所在路径复制粘贴到命令提示符工具中，后面加上“\mysqld --initialize-insecure”命令，进行初始化(在此之前，一定要进行第3步中的data文件操作，否则就会报错)。

进行以上操作后，若是在新建的data文件夹中出现以下几个文件夹，则说明初始化完成。同时也创建了一个用户名“root”,且密码为空。

# 5.服务端启动、客户端连接操作：
启动服务端：通过bin的路径+mysqld命令；
启动客户端：通过bin的路径+mysql命令-u 用户名(root)-p 密码(空)；

# 6.简单操作

show databases;             ==>查看目录下有哪些文件夹(数据库)

create database auth_db;    ==>创建一个新的数据库文件夹auth_db
drop database auth_db;      ==>删除数据库 auth_db

use auth_db；               ==>使用auth_db这个数据库

show tables；               ==>查看auth_db数据库中有哪些数据表

create table tb1;           ==>创建一个新的数据表tb1

select * from tb1；         ==>查看tb1数据表中的所有内容

进入dos界面，登录数据库，输入命令：show variables like "%char%"; 显示编码；

# 7.至此，MySQL已经完全安装，并且初始化完成了。

