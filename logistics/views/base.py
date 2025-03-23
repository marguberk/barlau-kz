from rest_framework import viewsets, permissions
from django.conf import settings

class BaseModelViewSet(viewsets.ModelViewSet):
    """Базовый класс для всех представлений с общей логикой"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
            
        queryset = self.queryset
        
        # Если режим отладки и метод GET, разрешаем получение данных без аутентификации
        if settings.DEBUG and self.request.method == 'GET' and not self.request.user.is_authenticated:
            return queryset
            
        if not self.request.user.is_authenticated:
            return self.queryset.none()
            
        return self.filter_queryset_by_role(queryset)
    
    def filter_queryset_by_role(self, queryset):
        """Переопределите этот метод в дочерних классах для фильтрации по ролям"""
        return queryset
    
    def perform_create(self, serializer):
        """Автоматически устанавливаем created_by при создании"""
        serializer.save(created_by=self.request.user) 