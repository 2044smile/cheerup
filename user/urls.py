from django.urls import path, include
from rest_framework import permissions

from . import views


urlpatterns = [
    path('signup/', views.UserSignUpAPIView.as_view()),
    path('signin/', views.UserSignInAPIView.as_view())
]