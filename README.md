# Cheer Up!

### Install

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
1. permissions.py 구현 💡
2. exceptions.py 구현
3. validators.py 구현 💡

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