from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.UserSignUpAPIView.as_view()),
    path('signin/', views.UserSignInAPIView.as_view()),
    path('destroy/', views.UserDestroyAPIView.as_view()),
]