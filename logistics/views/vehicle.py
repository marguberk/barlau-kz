from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django.utils import timezone
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
    
    @action(detail=True, methods=['get'])
    def gps_data(self, request, pk=None):
        """Получить GPS данные транспортного средства"""
        vehicle = self.get_object()
        
        if not vehicle.gps_enabled or not vehicle.gps_device_id:
            return Response(
                {"detail": "GPS мониторинг не настроен для этого транспортного средства"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Возвращаем текущие GPS данные
        gps_data = {
            'device_id': vehicle.gps_device_id,
            'latitude': float(vehicle.gps_latitude) if vehicle.gps_latitude else None,
            'longitude': float(vehicle.gps_longitude) if vehicle.gps_longitude else None,
            'speed': float(vehicle.gps_speed) if vehicle.gps_speed else None,
            'heading': float(vehicle.gps_heading) if vehicle.gps_heading else None,
            'altitude': float(vehicle.gps_altitude) if vehicle.gps_altitude else None,
            'satellites': vehicle.gps_satellites,
            'signal_quality': vehicle.gps_signal_quality,
            'fuel_level': float(vehicle.gps_fuel_level) if vehicle.gps_fuel_level else None,
            'engine_status': vehicle.gps_engine_status,
            'ignition_status': vehicle.gps_ignition_status,
            'last_update': vehicle.gps_last_update,
            'enabled': vehicle.gps_enabled
        }
        
        return Response(gps_data)
    
    @action(detail=True, methods=['post'])
    def sync_gps(self, request, pk=None):
        """Синхронизировать GPS данные транспортного средства"""
        if not request.user.role in ['DIRECTOR', 'SUPERADMIN', 'DISPATCHER']:
            return Response(
                {"detail": "У вас нет прав для синхронизации GPS данных"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        vehicle = self.get_object()
        
        if not vehicle.gps_device_id:
            return Response(
                {"detail": "GPS устройство не привязано к этому транспортному средству"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from logistics.services.stavtrack_service import StavTrackService
            stavtrack_service = StavTrackService()
            
            # Получаем актуальные данные от StavTrack
            position = stavtrack_service.get_vehicle_position(vehicle.gps_device_id)
            
            if position:
                # Обновляем данные в базе
                vehicle.gps_latitude = position.get('latitude')
                vehicle.gps_longitude = position.get('longitude')
                vehicle.gps_speed = position.get('speed')
                vehicle.gps_heading = position.get('course')
                vehicle.gps_altitude = position.get('altitude')
                vehicle.gps_satellites = position.get('satellites')
                vehicle.gps_signal_quality = position.get('signalQuality')
                vehicle.gps_fuel_level = position.get('fuelLevel')
                vehicle.gps_engine_status = position.get('engineStatus')
                vehicle.gps_ignition_status = position.get('ignitionStatus')
                vehicle.gps_last_update = timezone.now()
                vehicle.gps_enabled = True
                
                vehicle.save()
                
                return Response({
                    "detail": "GPS данные успешно синхронизированы",
                    "last_update": vehicle.gps_last_update
                })
            else:
                return Response(
                    {"detail": "Не удалось получить GPS данные от StavTrack"},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
                
        except Exception as e:
            logger.error(f"Ошибка при синхронизации GPS для {vehicle.number}: {str(e)}")
            return Response(
                {"detail": f"Ошибка при синхронизации GPS данных: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def perform_create(self, serializer):
        vehicle = serializer.save(created_by=self.request.user)
        Notification.create_vehicle_notification(self.request.user, vehicle)
        if vehicle.driver and vehicle.driver != self.request.user:
            Notification.create_vehicle_notification(vehicle.driver, vehicle) 