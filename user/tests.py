from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User


class UserModelTest(APITestCase):
    @classmethod
    def setUpTestData(cls):  # 초기화 한번만 실행
        cls.client = APIClient()

    def setUp(self):
        # 유저 인스턴스 생성
        self.client.post('/user/signup/', data={'email': 'dlckdtjr@naver.com', 'password': 'Dlckdtjr!1'})
        # 유저 인스턴스 저장
        user = User.objects.get(email='dlckdtjr@naver.com')
        
        refresh = RefreshToken.for_user(user=user)
        self.access = refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')

    # 회원가입 API를 테스트하는 코드
    def test_success_signup(self):
        response = self.client.post('/user/signup/', data={'email': 'first@naver.com', 'password': 'Dlckdtjr!1'})
        self.assertEqual(response.status_code, 201)

    def test_failed_signup(self):
        response = self.client.post('/user/signup/', data={'email': 'firstnaver.com', 'password': 'asdf'})
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/user/signup/', data={'email': 'first@naver.com', 'password': 'asdf'})
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/user/signup/', data={'email': 'first@naver.com', 'password': 'asdfasdf'})
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/user/signup/', data={'email': 'first@naver.com', 'password': 'asdfasdf1'})
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/user/signup/', data={'email': 'first@naver.com', 'password': 'asdfasdf1A'})
        self.assertEqual(response.status_code, 400)
        # 대문자, 소문자, 숫자, 특수문자가 모두 포함되어야 함
        response = self.client.post('/user/signup/', data={'email': 'first@naver.com', 'password': 'asdfasdf1A!'})
        self.assertEqual(response.status_code, 201)

    # 로그인 API를 테스트하는 코드
    def test_success_signin(self):
        response = self.client.post('/user/signin/', data={'email': 'dlckdtjr@naver.com', 'password': 'Dlckdtjr!1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id')
        self.assertContains(response, 'access')
        self.assertContains(response, 'refresh')

    def test_failed_signin(self):
        response = self.client.post('/user/signin/', data={'email': 'dlckdtjrnaver.com', 'password': 'Dlckdtjr!1'})
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/user/signin/', data={'email': 'dlckdtjr@naver.com', 'password': 'dlckdtjr'})
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/user/signin/', data={'email': 'dlckdtjr@naver.com', 'password': 'dlckdtjr!'})
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/user/signin/', data={'email': 'dlckdtjr@naver.com', 'password': 'dlckdtjr!1'})
        self.assertEqual(response.status_code, 400)

    # 회원탈퇴 API를 테스트하는 코드
    def test_success_destroy(self):
        response = self.client.delete('/user/destroy/', data={'email': 'dlckdtjr@naver.com', 'password': 'Dlckdtjr!1'}, HTTP_AUTHORIZATION=f'Bearer {self.access}')
        self.assertEqual(response.status_code, 204)

    def test_failed_destroy(self):
        response = self.client.delete('/user/destroy/', data={'email': 'dlckdtjrnaver.com', 'password': 'Dlckdtjr!1'})
        self.assertEqual(response.status_code, 400)
        response = self.client.delete('/user/destroy/', data={'email': 'dlckdtjr@naver.com', 'password': 'dlckdtjr'}, HTTP_AUTHORIZATION=f'Bearer {self.access}')
        self.assertEqual(response.status_code, 400)
        response = self.client.delete('/user/destroy/', data={'email': 'dlckdtjr@naver.com', 'password': 'dlckdtjr!'}, HTTP_AUTHORIZATION=f'Bearer {self.access}')
        self.assertEqual(response.status_code, 400)
        response = self.client.delete('/user/destroy/', data={'email': 'dlckdtjr@naver.com', 'password': 'dlckdtjr!1'}, HTTP_AUTHORIZATION=f'Bearer {self.access}')
        self.assertEqual(response.status_code, 400)
