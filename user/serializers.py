from rest_framework import serializers

from .models import User


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
            password=validated_data['password'],
            username=validated_data['username']
        )

        return user


class UserSignUpResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username']


class UserSignInSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    # def validate(self, data):  # serializer 는 데이터 검증 및 사용자 인증
    #     email = data.get('email', None)
    #     password = data.get('password', None)

    #     if email is not None and password is not None:
