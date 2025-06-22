from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from ..models import Task, TaskFile
from ..serializers import TaskSerializer, TaskFileSerializer
from .base import BaseModelViewSet
from django.conf import settings
from core.models import Notification
from django.db.models import Q
import os
import mimetypes

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
    queryset = Task.objects.select_related('assigned_to', 'created_by', 'vehicle').prefetch_related('assignees', 'files').all().order_by('-created_at')
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
        
        # Фильтрация по ролям:
        # - Водители видят только свои задачи
        # - Директора, Админы и Суперадмины видят все задачи
        # - Остальные роли видят задачи, которые создали или которые им назначены
        if user.role == 'DRIVER':
            return queryset.filter(Q(assigned_to=user) | Q(assignees=user)).distinct()
        elif user.role in ['DIRECTOR', 'ADMIN', 'SUPERADMIN']:
            # Показываем все задачи без фильтрации
            return queryset
        else:
            # Для остальных ролей - задачи которые создали или им назначены
            return queryset.filter(
                Q(created_by=user) | Q(assigned_to=user) | Q(assignees=user)
            ).distinct()
    
    def perform_create(self, serializer):
        task = serializer.save(created_by=self.request.user)
        # Создаем уведомления для всех исполнителей
        all_assignees = task.get_all_assignees()
        for assignee in all_assignees:
            if assignee != task.created_by:
                try:
                    Notification.create_task_notification(assignee, task)
                except Exception as e:
                    print(f"Ошибка создания уведомления: {e}")
    
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
        all_assignees = task.get_all_assignees()
        if (request.user.role not in ['DIRECTOR', 'SUPERADMIN'] and 
            request.user not in all_assignees):
            return Response(
                {"detail": "У вас нет прав для изменения статуса этой задачи"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        task.status = new_status
        task.save()
        
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_file(self, request, pk=None):
        """Загрузить файл к задаче"""
        task = self.get_object()
        
        if 'file' not in request.FILES:
            return Response(
                {"detail": "Файл не найден"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        uploaded_file = request.FILES['file']
        
        # Проверяем размер файла (максимум 10MB)
        if uploaded_file.size > 10 * 1024 * 1024:
            return Response(
                {"detail": "Размер файла не должен превышать 10MB"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Определяем тип файла
        file_type, _ = mimetypes.guess_type(uploaded_file.name)
        if not file_type:
            file_type = 'application/octet-stream'
        
        # Создаем запись о файле
        task_file = TaskFile.objects.create(
            task=task,
            file=uploaded_file,
            original_name=uploaded_file.name,
            file_type=file_type,
            file_size=uploaded_file.size,
            uploaded_by=request.user
        )
        
        serializer = TaskFileSerializer(task_file)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def files(self, request, pk=None):
        """Получить все файлы задачи"""
        task = self.get_object()
        files = task.files.all()
        serializer = TaskFileSerializer(files, many=True)
        return Response(serializer.data)


class TaskFileViewSet(BaseModelViewSet):
    queryset = TaskFile.objects.all().order_by('-uploaded_at')
    serializer_class = TaskFileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_task(self):
        """Получить задачу из URL параметра"""
        task_id = self.kwargs.get('task_id')
        if task_id:
            return get_object_or_404(Task, id=task_id)
        return None
    
    def get_queryset(self):
        """Фильтруем файлы по конкретной задаче"""
        task = self.get_task()
        if task:
            return self.queryset.filter(task=task)
        
        if not self.request.user.is_authenticated:
            return self.queryset.none()
        
        user = self.request.user
        if user.role in ['DIRECTOR', 'ADMIN', 'SUPERADMIN']:
            return self.queryset
        else:
            # Показываем только файлы задач, к которым у пользователя есть доступ
            accessible_tasks = Task.objects.filter(
                Q(created_by=user) | Q(assigned_to=user) | Q(assignees=user)
            ).distinct()
            return self.queryset.filter(task__in=accessible_tasks)
    
    def create(self, request, *args, **kwargs):
        """Создать файл для конкретной задачи"""
        task = self.get_task()
        if not task:
            return Response(
                {"detail": "Задача не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if 'file' not in request.FILES:
            return Response(
                {"detail": "Файл не найден"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        uploaded_file = request.FILES['file']
        
        # Проверяем размер файла (максимум 10MB)
        if uploaded_file.size > 10 * 1024 * 1024:
            return Response(
                {"detail": "Размер файла не должен превышать 10MB"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Определяем тип файла
        file_type, _ = mimetypes.guess_type(uploaded_file.name)
        if not file_type:
            file_type = 'application/octet-stream'
        
        # Создаем запись о файле
        task_file = TaskFile.objects.create(
            task=task,
            file=uploaded_file,
            original_name=uploaded_file.name,
            file_type=file_type,
            file_size=uploaded_file.size,
            uploaded_by=request.user
        )
        
        serializer = self.get_serializer(task_file)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        """Удалить файл (только создатель файла или админ)"""
        task_file = self.get_object()
        
        if (request.user != task_file.uploaded_by and 
            request.user.role not in ['DIRECTOR', 'ADMIN', 'SUPERADMIN']):
            return Response(
                {"detail": "У вас нет прав для удаления этого файла"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Удаляем физический файл
        if task_file.file and os.path.isfile(task_file.file.path):
            os.remove(task_file.file.path)
        
        return super().destroy(request, *args, **kwargs) 