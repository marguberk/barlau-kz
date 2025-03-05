from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from ..models import Task
from ..serializers import TaskSerializer
from .base import BaseModelViewSet

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
    
    def filter_queryset_by_role(self, queryset):
        user = self.request.user
        if user.role == 'DRIVER':
            return queryset.filter(assigned_to=user)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
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