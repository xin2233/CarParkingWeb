from django.test import TestCase, override_settings

from captcha.models import CaptchaStore
from login import models

DEVICE_KEY = '123'
DEVICE_TOKEN = 'test-token'


def captcha_data():
    """生成一对可通过校验的验证码参数（配合 CAPTCHA_TEST_MODE）"""
    hashkey = CaptchaStore.generate_key()
    response = CaptchaStore.objects.get(hashkey=hashkey).response
    return {'captcha_0': hashkey, 'captcha_1': response}


@override_settings(DEVICE_KEY=DEVICE_KEY, DEVICE_TOKEN=DEVICE_TOKEN, CAPTCHA_TEST_MODE=True)
class DeviceApiTests(TestCase):
    """设备接口：token 鉴权与状态读写"""

    def setUp(self):
        models.UserDetail.objects.create(
            device_key=DEVICE_KEY, tem='1', hum='1', bright='0', car_status='0')

    def test_getex_requires_token(self):
        resp = self.client.post('/getex/', {'key': DEVICE_KEY, 'bright': '1'})
        self.assertEqual(resp.content, b'0')

    def test_getex_with_token_updates_bright(self):
        resp = self.client.post('/getex/', {'key': DEVICE_KEY, 'bright': '1', 'token': DEVICE_TOKEN})
        self.assertEqual(resp.content, b'1')
        self.assertEqual(models.UserDetail.objects.get(device_key=DEVICE_KEY).bright, '1')

    def test_motor_requires_token(self):
        resp = self.client.get('/motor/')
        self.assertEqual(resp.content, b'0')

    def test_motor_reports_status(self):
        resp = self.client.get('/motor/', {'token': DEVICE_TOKEN})
        self.assertEqual(resp.content, b'2')  # 未预约
        models.UserDetail.objects.filter(device_key=DEVICE_KEY).update(car_status='1')
        resp = self.client.get('/motor/', {'token': DEVICE_TOKEN})
        self.assertEqual(resp.content, b'3')  # 已预约

    def test_motor_missing_device_record(self):
        models.UserDetail.objects.all().delete()
        resp = self.client.get('/motor/', {'token': DEVICE_TOKEN})
        self.assertEqual(resp.content, b'0')


@override_settings(DEVICE_KEY=DEVICE_KEY, DEVICE_TOKEN=DEVICE_TOKEN, CAPTCHA_TEST_MODE=True)
class AuthFlowTests(TestCase):
    """注册 / 登录 / 登出 / 登录保护"""

    def setUp(self):
        models.UserDetail.objects.create(
            device_key=DEVICE_KEY, tem='1', hum='1', bright='0', car_status='0')
        self.register_data = {
            'username': 'alice',
            'password1': 'Str0ngPass!x',
            'password2': 'Str0ngPass!x',
            'email': 'alice@example.com',
            'sex': 'female',
            **captcha_data(),
        }

    def test_register_creates_auth_user(self):
        resp = self.client.post('/register/', self.register_data)
        self.assertRedirects(resp, '/login/')
        from django.contrib.auth.models import User
        user = User.objects.get(username='alice')
        self.assertEqual(user.email, 'alice@example.com')
        self.assertTrue(models.Profile.objects.filter(user=user, sex='female').exists())

    def test_register_duplicate_username(self):
        self.client.post('/register/', self.register_data)
        resp = self.client.post('/register/', {
            **self.register_data, 'email': 'other@example.com', **captcha_data()})
        self.assertContains(resp, '用户名或邮箱已被注册')

    def test_login_logout(self):
        self.client.post('/register/', self.register_data)
        resp = self.client.post('/login/', {
            'username': 'alice', 'password': 'Str0ngPass!x', **captcha_data()})
        self.assertRedirects(resp, '/index/')
        resp = self.client.get('/logout/')
        self.assertEqual(resp.status_code, 302)  # 登出后跳 /index/（未登录会继续跳登录页，不再跟随）
        resp = self.client.get('/index/')
        self.assertRedirects(resp, '/login/?next=/index/')

    def test_login_wrong_password(self):
        self.client.post('/register/', self.register_data)
        resp = self.client.post('/login/', {
            'username': 'alice', 'password': 'wrong-pass', **captcha_data()})
        self.assertContains(resp, '用户名或密码不正确')

    def test_index_requires_login(self):
        resp = self.client.get('/index/')
        self.assertRedirects(resp, '/login/?next=/index/')

    def test_postex_requires_login(self):
        resp = self.client.post('/postex/')
        self.assertRedirects(resp, '/login/?next=/postex/')

    def test_postex_toggles_car_status(self):
        self.client.post('/register/', self.register_data)
        self.client.post('/login/', {
            'username': 'alice', 'password': 'Str0ngPass!x', **captcha_data()})
        self.client.post('/postex/')
        self.assertEqual(models.UserDetail.objects.get(device_key=DEVICE_KEY).car_status, '1')
        self.client.post('/postex/')
        self.assertEqual(models.UserDetail.objects.get(device_key=DEVICE_KEY).car_status, '0')
