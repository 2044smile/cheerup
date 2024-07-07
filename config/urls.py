from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView


schema_view = get_schema_view(
    openapi.Info(
        title="Cheer UP API",
        default_version='v1',
        description="Cheer UP API docs",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="master@master.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path(r'swagger$<format>\.json|\.yaml', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('user/', include('user.urls')),
    path('post/', include('post.urls')),
]