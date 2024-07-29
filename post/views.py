from django.utils.decorators import method_decorator
from rest_framework import serializers, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from config.exceptions import PostNotFoundException, PostPermissionDeniedException
from post.models import Post
from config.permissions import IsAuthenticatedAndOwner
from post.serializers import PostDetailResponseSerializer, PostListResponseSerializer, PostSerializer, PostResponseSerializer


@method_decorator(name='create', decorator=swagger_auto_schema(operation_id='게시글 생성', tags=['post']))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_id='게시글 수정', tags=['post']))
@method_decorator(name='list', decorator=swagger_auto_schema(operation_id='게시글 목록', 
                                                                    manual_parameters=[
                                                                        openapi.Parameter(
                                                                            'ordering', openapi.IN_QUERY, description="정렬 기준 (view_count, created_at)", 
                                                                            type=openapi.TYPE_STRING
                                                                        ),
                                                                    ],
                                                                    tags=['post']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_id='게시글 조회', tags=['post']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(operation_id='게시글 삭제', tags=['post']))
class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    http_method_names = ['get', 'post', 'put', 'delete']  # 설정한 메소드만 사용 가능
    pagination_class = PageNumberPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'view_count']  # ?ordering=view_count, ?ordering=-created_at query_params 로 가능
    ordering = ['-created_at']  # 기본 정렬

    def get_queryset(self):
        return Post.objects.select_related('user').all()

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action == 'update':
            return [IsAuthenticatedAndOwner()]  # custom 게시글 작성자만 가능
        if self.action == 'destroy':
            return [IsAuthenticatedAndOwner()]  # custom 게시글 작성자만 가능
        if self.action == 'list':
            return [AllowAny()]
        if self.action == 'retrieve':
            return [AllowAny()]

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post = Post.objects.create(title=serializer.validated_data['title'], content=serializer.validated_data['content'], user=request.user)

        response = PostResponseSerializer(post)

        return Response(response.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk, user=request.user)
        except Post.DoesNotExist:
            raise PostNotFoundException
        
        serializer = PostSerializer(data=request.data)
        
        if serializer.is_valid():
            post.title = serializer.validated_data['title']
            post.content = serializer.validated_data['content']
            post.save()

            response = PostResponseSerializer(post)

            return Response(response.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk, user=request.user)
        except Post.DoesNotExist:
            raise PostPermissionDeniedException

        post.delete()

        return Response({'204': 'ok'}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        posts = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(posts)

        if page is not None:
            serializer = PostListResponseSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PostListResponseSerializer(posts, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise PostNotFoundException

        post = self.get_queryset().get(pk=pk)
        post.view_count += 1
        post.save(update_fields=['view_count'])  # UPDATE post SET view_count = view_count + 1 WHERE id = pk

        serializer = PostDetailResponseSerializer(post)

        return Response(serializer.data)
