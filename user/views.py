from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema

from config.exceptions import UserNotFoundException, UserPasswordNotMatchException, UserAlreadyExistsException
from config.permissions import IsAuthenticatedAndOwner
from .models import User
from .serializers import UserSignInResponseSerializer, UserSignInSerializer, UserSignUpSerializer, UserSignUpResponseSerializer, UserDestroySerializer


class UserSignUpAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_id='회원가입', tags=['user'], request_body=UserSignUpSerializer, responses={'200': UserSignUpResponseSerializer})
    def post(self, request):
        if User.objects.filter(email=request.data['email']).exists():
            raise UserAlreadyExistsException
        
        serializer = UserSignUpSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSignInAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_id='로그인', tags=['user'], request_body=UserSignInSerializer, responses={'200': UserSignInResponseSerializer})
    def post(self, request):
        serializer = UserSignInSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
            except User.DoesNotExist:  # email 확인
                raise UserNotFoundException

            if not user.check_password(serializer.validated_data['password']):  # password 일치하는지 확인
                raise UserPasswordNotMatchException
            
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            # rest_framework_simplejwt/tokens.py
            # lifetime = api_settings.REFRESH_TOKEN_LIFETIME, access_token = api_settings.ACCESS_TOKEN_LIFETIME 즉, settings.py 에 설정 된 시간을 가져온다.

            return Response({'id': user.id, 'refresh': str(refresh), 'access': str(access_token)})
        else:
            return Response({'error': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)


class UserDestroyAPIView(APIView):
    permission_classes = [IsAuthenticatedAndOwner]

    @swagger_auto_schema(operation_id='회원 탈퇴', tags=['user'], request_body=UserDestroySerializer, responses={'200': UserSignUpResponseSerializer})
    def delete(self, request):
        serializer = UserDestroySerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
            except User.DoesNotExist:  # email 확인
                raise UserNotFoundException

            if not user.check_password(serializer.validated_data['password']):  # password 일치하는지 확인
                raise UserPasswordNotMatchException
            
            user = request.user
            user.is_active = False
            user.username = '탈퇴한 회원'
            user.save()
        
            return Response({'204': 'ok'}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
