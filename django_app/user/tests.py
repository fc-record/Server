from django.test import LiveServerTestCase
from rest_framework import status


class UserTest(LiveServerTestCase):
    def test_create_user(self):
        url = 'http://localhost:8000/api/users/'
        username = ['testuser1', 'testuser1@gmail.com']
        password = 'testpassword1'
        user_type = ['NORMAL', 'GOOGLE', 'FACEBOOK']
        nickname = 'testnickname'

        # 일반 계정(user_type = NORMAL)의 username이 email형식으로 작성 되었을 경우
        response = self.client.post(url, data={'username': username[1],
                                               'password': password,
                                               'user_type': user_type[0],
                                               'nickname': nickname})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertIn('token', response.data.keys())
        self.assertIn(username[1], response.data['user'].values())
        self.assertIn('nickname', response.data['user'].keys())
        self.assertIn('user_type', response.data['user'].keys())

        # 일반 계정의(user_type = NORMAL) username이 email형식으로 작성되지 않았을 경우
        response = self.client.post(url, data={'username': username[0],
                                               'password': password,
                                               'user_type': user_type[0],
                                               'nickname': nickname})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('유효한 이메일 주소를 입력하십시오.', response.data['email'])

        #
