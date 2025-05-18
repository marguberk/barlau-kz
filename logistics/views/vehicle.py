from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from ..models import Vehicle
from ..serializers import VehicleSerializer, VehicleLocationSerializer
from .base import BaseModelViewSet
from django.conf import settings
import logging
from core.models import Notification

class IsDirectorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.role in ['DIRECTOR', 'SUPERADMIN'] or request.user.is_superuser

class VehicleFilter(filters.FilterSet):
    min_year = filters.NumberFilter(field_name="year", lookup_expr='gte')
    max_year = filters.NumberFilter(field_name="year", lookup_expr='lte')
    
    class Meta:
        model = Vehicle
        fields = {
            'brand': ['exact', 'icontains'],
            'model': ['exact', 'icontains'],
            'number': ['exact', 'icontains'],
            'driver': ['exact', 'isnull'],
            'year': ['exact']
        }

class VehicleViewSet(BaseModelViewSet):
    queryset = Vehicle.objects.all().order_by('number')
    serializer_class = VehicleSerializer
    permission_classes = [permissions.AllowAny]  # Разрешаем доступ всем пользователям для чтения
    filterset_class = VehicleFilter
    
    def get_permissions(self):
        """
        Переопределение прав доступа:
        - Получение списка и деталей доступно всем
        - Изменение и добавление доступно только аутентифицированным с правами
        """
        if self.action in ['list', 'retrieve', 'locations']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsDirectorOrReadOnly()]
    
    def get_queryset(self):
        """
        Переопределяем метод для обеспечения корректной работы с анонимными пользователями
        """
        logger = logging.getLogger('django')
        
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
            
        queryset = self.queryset
        total_count = queryset.count()
        logger.debug(f"VehicleViewSet.get_queryset: total_count={total_count}")
        
        # Временный обходной путь - всегда возвращаем все транспортные средства для отладки
        return queryset  
        
        # Предыдущая логика (закомментирована на время отладки)
        # # Разрешаем неаутентифицированным пользователям получать данные, но только для чтения
        # if not self.request.user.is_authenticated:
        #     # Для просмотра транспорта не требуется аутентификация
        #     logger.debug("VehicleViewSet: user is not authenticated, returning all vehicles")
        #     return queryset
        # 
        # logger.debug(f"VehicleViewSet: user is authenticated, role={self.request.user.role}")
        # return self.filter_queryset_by_role(queryset)
    
    def filter_queryset_by_role(self, queryset):
        # Логирование для отладки
        logger = logging.getLogger('django')
        
        count_before = queryset.count()
        logger.debug(f"VehicleViewSet.filter_queryset_by_role: count_before={count_before}")
        
        # Для водителей показываем только их транспорт
        if self.request.user.is_authenticated and self.request.user.role == 'DRIVER':
            filtered_queryset = queryset.filter(driver=self.request.user)
            logger.debug(f"VehicleViewSet: user is DRIVER, filtered_count={filtered_queryset.count()}")
            return filtered_queryset
            
        # Для всех остальных - весь транспорт
        logger.debug(f"VehicleViewSet: returning all vehicles, count={queryset.count()}")
        return queryset
    
    @action(detail=False, methods=['get'])
    def locations(self, request):
        """Получить местоположение всех транспортных средств"""
        vehicles = Vehicle.objects.filter(driver__isnull=False)
        if request.user.role == 'DRIVER':
            vehicles = vehicles.filter(driver=request.user)
            
        serializer = VehicleLocationSerializer(vehicles, many=True)
        return Response(serializer.data)
        
    @action(detail=True, methods=['post'])
    def assign_driver(self, request, pk=None):
        """Назначить водителя на транспортное средство"""
        if not request.user.role in ['DIRECTOR', 'SUPERADMIN']:
            return Response(
                {"detail": "У вас нет прав для назначения водителей"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        vehicle = self.get_object()
        driver_id = request.data.get('driver_id')
        
        if not driver_id:
            return Response(
                {"detail": "Необходимо указать driver_id"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        vehicle.driver_id = driver_id
        vehicle.save()
        
        serializer = self.get_serializer(vehicle)
        return Response(serializer.data)

    def perform_create(self, serializer):
        vehicle = serializer.save(created_by=self.request.user)
        Notification.create_vehicle_notification(self.request.user, vehicle)
        if vehicle.driver and vehicle.driver != self.request.user:
            Notification.create_vehicle_notification(vehicle.driver, vehicle) 