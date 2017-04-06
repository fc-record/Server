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
        self.assertEqual('유효한 이메일 주소를 입력하십시오.', response.data['email'])

    def test_nomal_user_login(self):
        self.create_user()
        url = self.url + '/rest-auth/login/'
        # 정상적인 로그인
        response = self.client.post(url, data={'username': self.username[1],
                                               'password': self.password})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn('key', response.data.keys())

        # username or password가 틀렸을 경우
        response = self.client.post(url, data={'username': self.username[0],
                                               'password': self.password})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn('non_field_errors', response.data.keys())
        self.assertIn("제공된 인증데이터(credentials)로는 로그인할 수 없습니다.", response.data['non_field_errors'])

        # password를 빈값일 경우
        response = self.client.post(url, data={'username': self.username[1],
                                               'password': ''})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn('password', response.data.keys())
        self.assertIn('이 칸은 blank일 수 없습니다.', response.data['password'])

    def test_user_logout(self):
        user = self.create_user()
        url = self.url + '/rest-auth/logout/'
        # 정상적인 로그아웃
        response = self.client.post(url, headers={'Authorization': user.data['key']})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn('Successfully logged out.', response.data['detail'])

        # Token Value가 정상적이지 않은경우
        response = self.client.post(url, headers={'Authorization': 'Token testtoken'})
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertIn('토큰이 유효하지 않습니다.', response.data['detail'])



