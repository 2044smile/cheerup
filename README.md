# Cheer Up!

### Install

- poetry 로 의존성 관리

```txt
python = "^3.10"
django = "^5.0.6"
drf-yasg = "^1.21.7"
djangorestframework = "^3.15.2"
djangorestframework-simplejwt = "^5.3.1"
```

### Using docker

```cmd
docker build -t v1.0.0 .
docker run -p 8000:8000 v1.0.0
```

## Feature

- 💡 는 득도(도를 얻다. 즉, 무언가를 깨달았다는 뜻. )의 표시 입니다. 

### config
1. permissions.py (인증과 소유권 확인) 구현 💡
    ```python
    from rest_framework.permissions import BasePermission, SAFE_METHODS


    class IsAuthenticatedAndOwner(BasePermission):
        def has_permission(self, request, view):
            return request.user and request.user.is_authenticated
        
        def has_object_permission(self, request, view, obj):
            if request.method in SAFE_METHODS:
                return True
            return obj.user == request.user  # 토큰이 검증되면, 그 토큰에 포함된 사용자(User)의 정보가 request.user 에 저장된다.
    ```
2. exceptions.py 구현
3. validators.py 구현 💡
    ```python
    # config/validators.py
    from django.core.exceptions import ValidationError
    from django.contrib.auth.password_validation import validate_password
    import re
    
    
    class CustomPasswordValidator:
        def __call__(self, value):
            try:
                validate_password(value)
            except ValidationError as e:
                raise ValidationError(str(e))
    
        def validate(self, password, user=None):
            if len(password) < 8:
                raise ValidationError("비밀번호는 8자리 이상이어야 합니다.")
            if not re.search(r"[a-z]", password):
                raise ValidationError("비밀번호는 소문자를 포함해야 합니다.")
            if not re.search(r"[A-Z]", password):
                raise ValidationError("비밀번호는 대문자를 포함해야 합니다.")
            if not re.search(r"[!@#$%^&*()]", password):
                raise ValidationError("비밀번호는 특수문자를 포함해야 합니다.")
    
        def get_help_text(self):
            return "비밀번호는 8자리 이상이며 영문, 숫자, 특수문자((!@#$%^&*()))를 포함해야 합니다"
        

    # user/serializers.py
    def validate(self, attrs):
        password = attrs['password']
        CustomPasswordValidator().validate(password=password)
        return attrs
    ```

### core/models.py 💡

- self._state.adding 은 맨 처음 생성 될 때 True 상태, 그 이후로는 False
- Post 뿐만 아니라 User도 기본적으로는 None 상태에서 업데이트가 발생하면 시간이 생성되도록 구현
```python
from django.utils import timezone
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self._state.adding:
            self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True
```

### post/views.py 💡

- method 마다 permissions 설정
```python
def get_permissions(self):
    if self.action == 'create':
        return [IsAuthenticated()]
    if self.action == 'update':
        return [IsAuthenticatedAndOwner()]  # custom
    if self.action == 'destroy':
        return [IsAuthenticatedAndOwner()]  # custom
    if self.action == 'list':
        return [AllowAny()]
    if self.action == 'retrieve':
        return [AllowAny()]
```

### tests.py

```python
python manage.py test  # rest_framework.test
```
