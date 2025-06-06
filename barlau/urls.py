"""
URL configuration for barlau project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView, TemplateView
from django.shortcuts import redirect
from core.views import FileUploadView

schema_view = get_schema_view(
    openapi.Info(
        title="Barlau.kz API",
        default_version='v1',
        description="API для логистической компании Barlau.kz",
        contact=openapi.Contact(email="contact@barlau.kz"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/upload/', FileUploadView.as_view(), name='file-upload'),
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('core:home'), name='index'),
    path('dashboard/', include('core.urls', namespace='core')),
    path('dashboard/new/', TemplateView.as_view(template_name='core/dashboard.html'), name='dashboard_new'),
    path('api/v1/', include('logistics.urls')),
    path('api/v1/', include('accounts.urls')),
    path('api/', include('logistics.urls')),
    path('', include('core.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Аутентификация
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
