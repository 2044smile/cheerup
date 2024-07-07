import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from core.models import BaseModel


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, password=None):
        if not email:
            raise ValueError("You must have an email address")
        
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password
        )
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, BaseModel):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=32, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"{self.email}"
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = uuid.uuid4().hex[:10]
        return super().save(*args, **kwargs)
