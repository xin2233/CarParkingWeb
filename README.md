# CarParkingWeb 停车场管理系统

基于 Django 的停车场**服务器端**项目。树莓派等设备端通过 HTTP 接口上报红外传感器数据、查询与切换车位预约状态；网页端提供用户注册/登录、车位状态展示与预约控制。前端基于 Bootstrap 3。

## 功能

- 用户注册 / 登录 / 登出（带图形验证码，`django-simple-captcha`）
- 车位状态展示：温度、湿度、红外信号（`bright`）、车位预约状态（`car_status`）
- 车位预约：网页按钮一键切换预约状态
- 设备端 HTTP 接口：数据上报、状态查询（见下文）
- Django Admin 后台：管理用户与设备信息

## 技术栈

| 组件 | 说明 |
| --- | --- |
| Django 4.2 | Web 框架（Python 3.8+，推荐 3.10+） |
| MySQL | 数据库（库名 `auth_db`） |
| django-simple-captcha | 登录/注册图形验证码 |
| Bootstrap 3.3.7 / jQuery 3.4.1 | 前端页面与交互 |
| uWSGI + Nginx | 生产部署（示例见 `uwsgi.ini`） |

## 快速开始

### 环境要求

- **Python 3.8+（推荐 3.10+）**，基于 Django 4.2 LTS。
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

### 3. 配置环境变量

| 环境变量 | 说明 | 默认值 |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Django 密钥，**生产环境必须设置** | 开发用占位值 |
| `DJANGO_DEBUG` | 设为 `0` 关闭调试模式 | `1`（开启） |
| `DJANGO_ALLOWED_HOSTS` | 逗号分隔的主机列表 | `127.0.0.1,localhost` |
| `DEVICE_KEY` | 设备标识 | `123` |
| `DEVICE_TOKEN` | 设备接口鉴权 token，**生产环境必须设置为随机长字符串** | `123` |

### 4. 初始化

```bash
python manage.py makemigrations   # 仓库不包含迁移文件（已被 .gitignore 排除），首次必须执行
python manage.py migrate
python manage.py createsuperuser  # 创建后台管理员
```

### 5. 运行

```bash
python manage.py runserver 0.0.0.0:8000
```

- 前台：<http://127.0.0.1:8000/>（注册账号后登录使用）
- 后台：<http://127.0.0.1:8000/admin/>

### 6. 初始化设备数据（必须！）

系统依赖一条 `device_key='123'`（与 `DEVICE_KEY` 一致）的设备记录，否则首页与设备接口会提示数据缺失。登录 Admin 后台，在「设备信息」中新增一条记录：

| 字段 | 值 |
| --- | --- |
| Device key | 123 |
| Tem | 1 |
| Hum | 1 |
| Bright | 1 |
| Car status | 0 |

## 设备端 HTTP 接口

设备端（树莓派等）与服务器交互的接口约定。**除网页调用的 `/postex/` 外，所有接口都需要鉴权**：在请求头携带 `X-Device-Token: <DEVICE_TOKEN>`，或在参数中携带 `token=<DEVICE_TOKEN>`；鉴权失败返回 `'0'`。

| 接口 | 方法 | 参数 | 说明 | 返回 |
| --- | --- | --- | --- | --- |
| `/getex/` | POST | `key`、`bright`、token | 设备上报红外数据，更新 `bright` 字段 | `'1'` 成功 / `'0'` 失败 |
| `/motor/` | GET | token | 查询当前车位预约状态 | `'2'` 未预约 / `'3'` 已预约 / `'0'` 失败 |
| `/postex/` | POST | 无（需 `csrf_token`，且需网页登录） | 网页「提交预约」按钮调用，切换 `car_status` | 重定向至 `/index/` |

其中 `/getex/`、`/motor/` 已加 `@csrf_exempt`，用 token 鉴权替代 CSRF；`/postex/` 由网页表单调用，需携带 CSRF Token。

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

## 账号体系说明

- 用户账号使用 **Django 内置认证**（`django.contrib.auth`），密码采用 Django 的 PBKDF2 哈希；性别等附加信息保存在 `login.models.Profile`。
- 通过 `createsuperuser` 创建的后台管理员同样可以登录 Web 端。
- 访问控制：首页与预约操作要求网页登录；设备接口要求 token。
- 运行测试无需 MySQL：`DJANGO_DB=sqlite python manage.py test login`。

## 部署（uWSGI + Nginx）

`uwsgi.ini` 已使用相对 `%(here)` 路径，将其复制到部署目录并按需调整后：

```bash
uwsgi --ini uwsgi.ini
```

Nginx 将请求反向代理至 `127.0.0.1:8000` 即可。生产环境务必通过环境变量设置新的 `DJANGO_SECRET_KEY`、随机 `DEVICE_TOKEN`，设置 `DJANGO_DEBUG=0` 并收紧 `DJANGO_ALLOWED_HOSTS`。

## 开源协议

本项目采用 [Apache License 2.0](LICENSE)。
