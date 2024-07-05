from rest_framework import serializers

from .models import User
from config.validators import CustomPasswordValidator


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
        fields = ['email', 'password', 'username']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.username = validated_data['username']

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
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']


class UserSignInResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username']
