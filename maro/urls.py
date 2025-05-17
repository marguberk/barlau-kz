from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import FileUploadView

urlpatterns = [
    path('api/upload/', FileUploadView.as_view(), name='file-upload'),  # СТАВИМ ПЕРВЫМ!
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('api/logistics/', include('logistics.urls', namespace='logistics-api')),
    path('', include('pwa.urls')),  # Добавляем URL-адреса PWA
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 