from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from ..models import Task
from ..serializers import TaskSerializer
from .base import BaseModelViewSet
from django.conf import settings
from core.models import Notification

class TaskFilter(filters.FilterSet):
    min_due_date = filters.DateTimeFilter(field_name="due_date", lookup_expr='gte')
    max_due_date = filters.DateTimeFilter(field_name="due_date", lookup_expr='lte')
    
    class Meta:
        model = Task
        fields = {
            'title': ['exact', 'icontains'],
            'status': ['exact'],
            'priority': ['exact'],
            'assigned_to': ['exact'],
            'vehicle': ['exact'],
            'created_by': ['exact']
        }

class TaskViewSet(BaseModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = TaskFilter
    
    def get_permissions(self):
        """
        Переопределяем получение разрешений для возврата тестовых данных неавторизованным пользователям
        """
        if self.request.method == 'GET' and settings.DEBUG:
            return []
        return [permission() for permission in self.permission_classes]
    
    def get_queryset(self):
        """
        Переопределяем метод для обеспечения корректной работы с анонимными пользователями
        """
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
            
        queryset = self.queryset
        
        if not self.request.user.is_authenticated and settings.DEBUG:
            # Для неавторизованных пользователей в режиме отладки возвращаем все задачи
            return queryset
        
        if not self.request.user.is_authenticated:
            return self.queryset.none()
            
        return self.filter_queryset_by_role(queryset)
    
    def filter_queryset_by_role(self, queryset):
        user = self.request.user
        if not user.is_authenticated and settings.DEBUG:
            # Для неавторизованных пользователей в режиме отладки возвращаем все задачи
            return queryset
        
        if user.role == 'DRIVER':
            return queryset.filter(assigned_to=user)
        return queryset
    
    def perform_create(self, serializer):
        task = serializer.save(created_by=self.request.user)
        # Уведомление только для исполнителя, если он назначен и это не создатель
        if task.assigned_to and task.assigned_to != task.created_by:
            Notification.create_task_notification(task.assigned_to, task)
    
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """Изменить статус задачи"""
        task = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return Response(
                {"detail": "Необходимо указать новый статус"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if new_status not in dict(Task.STATUS_CHOICES):
            return Response(
                {"detail": "Некорректный статус"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Проверяем права на изменение статуса
        if request.user.role not in ['DIRECTOR', 'SUPERADMIN'] and request.user != task.assigned_to:
            return Response(
                {"detail": "У вас нет прав для изменения статуса этой задачи"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        task.status = new_status
        task.save()
        
        serializer = self.get_serializer(task)
        return Response(serializer.data) 