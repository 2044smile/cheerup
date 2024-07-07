from django.db import models

from user.models import User
from core.models import BaseModel


class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    content = models.TextField()
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
