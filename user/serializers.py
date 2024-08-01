from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from config.validators import CustomPasswordValidator
from config.exceptions import UserNotFoundException, UserPasswordNotMatchException


class UserSignUpSerializer(serializers.ModelSerializer):
    """
    ### .create() 는 패스워드 암호화 `set_password`
    instance = User.objects.create(...)
    instance.set_password(password)
    instance.save()

    ### .create_user() 는 자동으로 암호화
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.username = validated_data.get('username')
        user.save()

        return user
        
    def validate(self, attrs):
        password = attrs['password']
        CustomPasswordValidator().validate(password=password)
        return attrs


class UserSignUpResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username']


class UserSignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'validators': []}
        }


class UserSignInResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username']


class UserDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'validators': []}
        }


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, required=False)
    new_password_confirm = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'current_password', 'new_password', 'new_password_confirm']
        extra_kwargs = {
            'username': {'required': False},
            'current_password': {'required': True},
            'new_password': {'required': False},
            'new_password_confirm': {'required': False}
        }

    def validate_current_password(self, value):
        user = self.instance
        if not check_password(value, user.password):
            raise serializers.ValidationError("Current password is not correct")
        return value

    def validate(self, data):
        # 새로운 비밀번호와 비밀번호 확인 일치 여부 확인
        if data.get('new_password') and data.get('new_password') != data.get('new_password_confirm'):
            raise serializers.ValidationError("New passwords do not match")
        return data

    def update(self, instance, validated_data):
        # 사용자 이름 업데이트
        instance.username = validated_data.get('username', instance.username)
        
        # 새로운 비밀번호 설정
        new_password = validated_data.get('new_password')
        if new_password:
            instance.set_password(new_password)
        
        # 사용자 정보 저장
        instance.save()
        return instance
