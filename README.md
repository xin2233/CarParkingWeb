# 智能停车场管理系统（CarParkingWeb）

基于 Django 的智能停车场 **服务器端** 项目。配套树莓派等设备端通过 HTTP 接口上报红外传感器数据、查询与切换车位预约状态；网页端提供用户注册/登录、设备状态展示与车位预约控制。前端基于 Bootstrap 3 实现。

> 本项目最初编写于 2021 年，是个人学习**物联网**时的服务器端实战项目：设备端（树莓派）采集红外传感器与温湿度数据上报至服务器，用户通过网页实时查看车位状态并远程预约车位。项目经调试后开源，**仅供学习交流使用**。

## 功能特性

- 用户注册 / 登录 / 登出（带图形验证码，`django-simple-captcha`）
- 设备状态实时展示：温度、湿度、红外信号（`bright`）、车位预约状态（`car_status`）
- 车位预约：网页按钮一键切换预约状态
- 设备端 HTTP 接口：数据上报、状态查询、预约控制（详见下文）
- Django Admin 后台：管理用户与设备信息

## 技术栈

| 组件 | 说明 |
| --- | --- |
| Django 2.2 | Web 框架（Python 3.8 / 3.9，见下文环境要求） |
| MySQL | 数据库（库名 `auth_db`） |
| django-simple-captcha | 登录/注册图形验证码 |
| Bootstrap 3.3.7 / jQuery 3.4.1 | 前端页面与交互 |
| uWSGI + Nginx | 生产部署（示例见 `uwsgi.ini`） |

## 快速开始

### 环境要求

- **Python 3.8 或 3.9（推荐）**。注意：Django 2.2 不支持 Python 3.10+（Django 2.2 官方支持 3.5–3.9）；若需在更高版本 Python 下运行，请升级 Django 至 4.2+ 并相应适配 `signup/settings.py`。
- MySQL 5.7+，可正常连接。

### 1. 安装依赖

```bash
git clone <your-repo-url>
cd CarParkingWeb
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 配置数据库

```bash
mysql -u root -p
CREATE DATABASE auth_db DEFAULT CHARACTER SET utf8mb4;
```

然后在 `signup/settings.py` 的 `DATABASES` 中，将 `USER` / `PASSWORD` / `HOST` / `PORT` 改为你本机的 MySQL 配置。

### 3. 初始化

```bash
python manage.py makemigrations   # 仓库不包含迁移文件（已被 .gitignore 排除），首次必须执行
python manage.py migrate
python manage.py createsuperuser  # 创建后台管理员
```

### 4. 运行

```bash
python manage.py runserver 0.0.0.0:8000
```

- 前台：<http://127.0.0.1:8000/>（注册账号后登录使用）
- 后台：<http://127.0.0.1:8000/admin/>

### 5. 初始化设备数据（必须！）

系统依赖一条 `device_key='123'` 的设备记录，否则首页与设备接口会直接报错。登录 Admin 后台，在「设备信息」中新增一条记录：

| 字段 | 值 |
| --- | --- |
| Device key | 123 |
| Tem | 1 |
| Hum | 1 |
| Bright | 1 |
| Car status | 1 |

> `'123'` 为代码中硬编码的设备号，如需修改请同步修改 `login/views.py`。

## 设备端 HTTP 接口

设备端（树莓派等）与服务器交互的接口约定：

| 接口 | 方法 | 参数 | 说明 | 返回 |
| --- | --- | --- | --- | --- |
| `/getex/` | POST | `key`、`bright` | 设备上报红外数据，更新 `bright` 字段 | `'1'` 成功 / `'0'` 失败 |
| `/motor/` | GET | 无 | 查询当前车位预约状态 | `'2'` 未预约 / `'3'` 已预约 |
| `/postex/` | POST | 无（需 `csrf_token`） | 网页「提交预约」按钮调用，切换 `car_status` | 重定向至 `/index/` |

其中 `/getex/` 已加 `@csrf_exempt`，无需 CSRF Token；`/postex/` 由网页表单调用，需携带 CSRF Token。

## 项目结构

```
CarParkingWeb/
├── manage.py          # Django 管理入口
├── requirements.txt   # Python 依赖清单
├── signup/            # 工程配置（settings / urls / wsgi）
├── login/             # 业务应用（模型 / 视图 / 表单 / 后台）
├── templates/         # 页面模板（base / index / login / register）
├── static/            # 静态资源（Bootstrap / jQuery / 图片）
└── uwsgi.ini          # uWSGI 部署示例
```

## 账号体系说明（重要）

- **Web 端注册的用户**保存在 `login.models.User`（自定义模型），密码使用 SHA-256 + 盐（`'mysite'`）哈希，与 Django 内置认证是**两套独立体系**。
- 通过 `createsuperuser` 创建的**后台管理员不能登录 Web 端**，反之亦然；后台账号仅用于 Admin 管理数据。
- 因此首次部署后，前台账号需要自己到注册页注册。

## 部署（uWSGI + Nginx）

`uwsgi.ini` 已使用相对 `%(here)` 路径，将其复制到部署目录并按需调整后：

```bash
uwsgi --ini uwsgi.ini
```

Nginx 将请求反向代理至 `127.0.0.1:8000` 即可。生产环境务必修改 `SECRET_KEY`、关闭 `DEBUG` 并收紧 `ALLOWED_HOSTS`。

## 开源协议

本项目采用 [Apache License 2.0](LICENSE)。
