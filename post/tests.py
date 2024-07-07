from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from post.models import Post
from user.models import User


class PostModelTest(APITestCase):

    @classmethod
    def setUpTestData(cls):  # 초기화 한번만 실행 / PostModelTest 함수 안에서 사용할 수 있는 변수 생성
        cls.user = User.objects.create(email='Tim', password='Tim1234!@#$')
        cls.post = Post.objects.create(title='cheer up!', content='I can do it', user=cls.user)
        cls.client = APIClient()

        refresh = RefreshToken.for_user(user=cls.user)
        cls.access = refresh.access_token
        cls.client.credentials(HTTP_AUTHORIZATION=f'Bearer {cls.access}')

    def test_updated_at_none(self):
        target = self.post.updated_at
        self.assertIsNone(target, "처음 생성 할 때는 None")

    def test_updated_at(self):
        response = self.client.put(f'/post/{self.post.id}/', data={'title': 'cheer up!!', 'content': 'I can do it!!'}, HTTP_AUTHORIZATION=f'Bearer {self.access}')
        target = Post.objects.get(id=self.post.id).updated_at
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(target, "수정 할 때는 날짜가 들어가야 함")

    # 게시글을 생성하는 API를 테스트하는 코드
    def test_success_create(self):
        response = self.client.post(f'/post/', data={'title': 'Come on!!', 'content': 'Dude!'}, HTTP_AUTHORIZATION=f'Bearer {self.access}')
        self.assertEqual(response.status_code, 201)
    
    def test_failed_create(self):
        response = self.client.post(f'/post/', data={'title': 'Come on!!'})  # 토큰이 존재하지 않습니다.
        self.assertEqual(response.status_code, 401)

    # 게시글 리스트를 가져오는 API를 테스트하는 코드
    def test_success_get_list(self):
        response = self.client.get(f'/post/')
        self.assertEqual(response.status_code, 200)

    # 게시글 상세를 가져오는 API를 테스트하는 코드
    def test_success_get_detail(self):
        response = self.client.get(f'/post/{self.post.id}/')
        self.assertEqual(response.status_code, 200)

    # 게시글 수정하는 API를 테스트하는 코드
    def test_success_put(self):
        response = self.client.put(f'/post/{self.post.id}/', data={'title': 'cheer up!!!', 'content': 'I can do it!!!'}, HTTP_AUTHORIZATION=f'Bearer {self.access}')
        self.assertEqual(response.status_code, 200)

    def test_failed_put(self):
        response = self.client.put(f'/post/{self.post.id}/', data={'title': 'cheer up!!!', 'content': 'I can do it!!!'})
        self.assertEqual(response.status_code, 401)

    # 게시글 삭제하는 API를 테스트하는 코드
    def test_success_delete(self):
        response = self.client.delete(f'/post/{self.post.id}/', HTTP_AUTHORIZATION=f'Bearer {self.access}')
        self.assertEquals(response.status_code, 204)

    def test_failed_delete(self):
        response = self.client.delete(f'/post/{self.post.id}/')
        self.assertEqual(response.status_code, 401)