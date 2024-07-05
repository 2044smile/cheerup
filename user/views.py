from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from .models import User
from .serializers import UserSignInResponseSerializer, UserSignInSerializer, UserSignUpSerializer, UserSignUpResponseSerializer


class UserSignUpAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_id='회원가입', tags=['user'], request_body=UserSignUpSerializer, responses={'200': UserSignUpResponseSerializer})
    def post(self, request):
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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
