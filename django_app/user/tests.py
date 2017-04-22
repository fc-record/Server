from django.test import LiveServerTestCase
from rest_framework import status


class UserTest(LiveServerTestCase):
    url = 'http://localhost:8000'
    username = ['testuser1', 'testuser1@gmail.com']
    password = 'testpassword1'
    user_type = ['NORMAL', 'GOOGLE', 'FACEBOOK']
    nickname = 'testnickname'

    def create_user(self):
        url = self.url + '/api/users/'
        user = self.client.post(url, data={'username': self.username[1],
                                           'password': self.password,
                                           'user_type': self.user_type[0],
                                           'nickname': self.nickname})
        return user

    def test_create_user(self):
        url = self.url + '/api/users/'

        # 일반 계정(user_type = NORMAL)의 username이 email형식으로 작성 되었을 경우
        response = self.client.post(url, data={'username': self.username[1],
                                               'password': self.password,
                                               'user_type': self.user_type[0],
                                               'nickname': self.nickname})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertIn('key', response.data.keys())
        self.assertIn(self.username[1], response.data['user'].values())
        self.assertIn(self.nickname, response.data['user'].values())
        self.assertIn(self.user_type[0], response.data['user'].values())

        # 일반 계정의(user_type = NORMAL) username이 email형식으로 작성되지 않았을 경우
        response = self.client.post(url, data={'username': self.username[0],
                                               'password': self.password,
                                               'user_type': self.user_type[0],
                                               'nickname': self.nickname})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Enter a valid email address.', response.data['detail'])

    def test_nomal_user_login(self):
        user = self.create_user()
        url = self.url + '/user/login/'
        # 정상적인 로그인
        response = self.client.post(url, data={'username': self.username[1],
                                               'password': self.password})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn('key', response.data.keys())
        self.assertIn('user', response.data.keys())

        # username or password가 틀렸을 경우
        response = self.client.post(url, data={'username': self.username[0],
                                               'password': self.password})
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertIn("Username or Password is wrong", response.data['detail'])

        # password를 빈값일 경우
        response = self.client.post(url, data={'username': self.username[1],
                                               'password': ''})
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertIn("Username or Password is wrong", response.data['detail'])

    def test_user_logout(self):
        user = self.create_user()
        url = self.url + '/user/logout/'
        # 정상적인 로그아웃
        response = self.client.post(url, HTTP_AUTHORIZATION='Token {}'.format(user.data['key']))
        print(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn('Logout Succeeded and Token Delete', response.data['detail'])

        # Token Value가 정상적이지 않은경우
        response = self.client.post(url, headers={'Authorization': 'testtoken'})
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertIn("Authentication credentials were not provided.", response.data['detail'])

    def test_check_token(self):
        user = self.create_user()
        url = self.url + '/user/token/'

        # 현재 유효한 토큰일 경우
        response = self.client.post(url, data={'key': user.data['key']})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('valid token', response.data['detail'])

        # 현재 유효하지 않은 토큰일 경우
        response = self.client.post(url, data={'key': 'testtoken'})
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual('Invalid token', response.data['detail'])

    def test_change_password(self):
        user = self.create_user()
        url = self.url + '/user/changepassword/'

        # 정상적으로 변경되었을 경우
        response = self.client.post(url, data={'change_password1': '1234qwer', 'change_password2': '1234qwer'},
                                    HTTP_AUTHORIZATION='Token {}'.format(user.data['key']))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # 변경할 비밀번호를 다르게 입력하거나 8자 미만일 경우
        response = self.client.post(url, data={'change_password1': '1234qwer', 'change_password2': '1234'},
                                    HTTP_AUTHORIZATION='Token {}'.format(user.data['key']))
        self.assertEqual('Password does not match or too short password', response.data['detail'])

    # def test_change_profile_img(self):
    #     user = self.create_user()
    #     url = self.url + '/user/changeprofile/'
    #     response = self.client.post(url, data={'photo': 'iu.jpg'},
    #                                 HTTP_AUTHORIZATION='Token {}'.format(user.data['key']))
    #     print(response.data)
