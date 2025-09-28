from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Vehicle, VehicleGPSHistory
# from .services.stavtrack_service import StavTrackService
from .services.wialon_service import WialonService
from .serializers import VehicleSerializer
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vehicle_gps_status(request, vehicle_id):
    """Получение текущего GPS статуса транспортного средства"""
    try:
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        
        if not vehicle.gps_enabled:
            return Response({
                'error': 'GPS мониторинг не включен для данного транспортного средства'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Обновляем GPS данные через Wialon API
        wialon_service = WialonService()
        if vehicle.gps_device_id:
            wialon_service.update_vehicle_gps_data(vehicle)
        
        # Возвращаем обновленные данные
        gps_data = {
            'vehicle_id': vehicle.id,
            'vehicle_number': vehicle.number,
            'gps_enabled': vehicle.gps_enabled,
            'gps_device_id': vehicle.gps_device_id,
            'gps_imei': vehicle.gps_imei,
            'gps_phone': vehicle.gps_phone,
            'last_update': vehicle.gps_last_update,
            'location': {
                'latitude': vehicle.gps_latitude,
                'longitude': vehicle.gps_longitude,
                'speed': vehicle.gps_speed,
                'heading': vehicle.gps_heading,
                'altitude': vehicle.gps_altitude,
            },
            'status': {
                'satellites': vehicle.gps_satellites,
                'signal_quality': vehicle.gps_signal_quality,
                'fuel_level': vehicle.gps_fuel_level,
                'engine_status': vehicle.gps_engine_status,
                'ignition_status': vehicle.gps_ignition_status,
            }
        }
        
        return Response(gps_data)
        
    except Exception as e:
        logger.error(f"Ошибка получения GPS статуса: {e}")
        return Response({
            'error': 'Ошибка получения GPS данных'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vehicle_gps_history(request, vehicle_id):
    """Получение истории GPS данных транспортного средства"""
    try:
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        
        if not vehicle.gps_enabled:
            return Response({
                'error': 'GPS мониторинг не включен для данного транспортного средства'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Получаем параметры фильтрации
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        limit = int(request.GET.get('limit', 100))
        
        # Фильтруем историю
        history_queryset = VehicleGPSHistory.objects.filter(vehicle=vehicle)
        
        if start_date:
            history_queryset = history_queryset.filter(timestamp__gte=start_date)
        if end_date:
            history_queryset = history_queryset.filter(timestamp__lte=end_date)
        
        history = history_queryset.order_by('-timestamp')[:limit]
        
        history_data = []
        for record in history:
            history_data.append({
                'timestamp': record.timestamp,
                'latitude': record.latitude,
                'longitude': record.longitude,
                'speed': record.speed,
                'heading': record.heading,
                'altitude': record.altitude,
                'satellites': record.satellites,
                'signal_quality': record.signal_quality,
                'fuel_level': record.fuel_level,
                'engine_status': record.engine_status,
                'ignition_status': record.ignition_status,
            })
        
        return Response({
            'vehicle_id': vehicle.id,
            'vehicle_number': vehicle.number,
            'history': history_data,
            'total_records': len(history_data)
        })
        
    except Exception as e:
        logger.error(f"Ошибка получения GPS истории: {e}")
        return Response({
            'error': 'Ошибка получения GPS истории'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sync_vehicle_gps(request, vehicle_id):
    """Синхронизация транспортного средства с GPS устройством"""
    try:
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        device_id = request.data.get('device_id')
        
        if not device_id:
            return Response({
                'error': 'Не указан ID GPS устройства'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        stavtrack_service = StavTrackService()
        success = stavtrack_service.sync_vehicle_with_device(vehicle, device_id)
        
        if success:
            return Response({
                'message': f'Транспорт {vehicle.number} успешно синхронизирован с GPS устройством {device_id}',
                'vehicle': VehicleSerializer(vehicle).data
            })
        else:
            return Response({
                'error': 'Ошибка синхронизации с GPS устройством'
            }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        logger.error(f"Ошибка синхронизации GPS: {e}")
        return Response({
            'error': 'Ошибка синхронизации'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sync_all_gps_wialon(request):
    """Синхронизация всех GPS данных с Wialon API"""
    try:
        wialon_service = WialonService()
        
        # Авторизация
        if not wialon_service.authenticate():
            return Response({
                'error': 'Ошибка авторизации в Wialon API'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Синхронизация всех грузовиков
        updated_count = wialon_service.sync_all_vehicles_gps()
        
        # Выход из системы
        wialon_service.logout()
        
        return Response({
            'message': f'Синхронизация завершена: обновлено {updated_count} грузовиков',
            'updated_count': updated_count
        })
        
    except Exception as e:
        logger.error(f"Ошибка синхронизации GPS с Wialon: {e}")
        return Response({
            'error': f'Ошибка синхронизации: {e}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def available_gps_devices(request):
    """Получение списка доступных GPS устройств"""
    try:
        stavtrack_service = StavTrackService()
        devices = stavtrack_service.get_available_devices()
        
        return Response({
            'devices': devices,
            'total_devices': len(devices),
            'available_devices': len([d for d in devices if not d['is_used']])
        })
        
    except Exception as e:
        logger.error(f"Ошибка получения доступных устройств: {e}")
        return Response({
            'error': 'Ошибка получения списка устройств'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_all_vehicles_gps(request):
    """Обновление GPS данных для всех транспортных средств"""
    try:
        stavtrack_service = StavTrackService()
        updated_count = stavtrack_service.update_all_vehicles_gps()
        
        return Response({
            'message': f'Обновлены GPS данные для {updated_count} транспортных средств',
            'updated_count': updated_count
        })
        
    except Exception as e:
        logger.error(f"Ошибка массового обновления GPS: {e}")
        return Response({
            'error': 'Ошибка обновления GPS данных'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vehicles_with_gps(request):
    """Получение списка транспортных средств с GPS мониторингом"""
    try:
        vehicles = Vehicle.objects.filter(gps_enabled=True)
        
        vehicles_data = []
        for vehicle in vehicles:
            vehicles_data.append({
                'id': vehicle.id,
                'number': vehicle.number,
                'brand': vehicle.brand,
                'model': vehicle.model,
                'driver': vehicle.driver.full_name if vehicle.driver else None,
                'gps_device_id': vehicle.gps_device_id,
                'gps_imei': vehicle.gps_imei,
                'gps_last_update': vehicle.gps_last_update,
                'location': {
                    'latitude': vehicle.gps_latitude,
                    'longitude': vehicle.gps_longitude,
                    'speed': vehicle.gps_speed,
                },
                'status': {
                    'fuel_level': vehicle.gps_fuel_level,
                    'engine_status': vehicle.gps_engine_status,
                    'ignition_status': vehicle.gps_ignition_status,
                }
            })
        
        return Response({
            'vehicles': vehicles_data,
            'total_vehicles': len(vehicles_data)
        })
        
    except Exception as e:
        logger.error(f"Ошибка получения транспорта с GPS: {e}")
        return Response({
            'error': 'Ошибка получения данных'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








































