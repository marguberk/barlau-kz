from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache
from django.db import transaction
from .serializers import UserUpdateSerializer, UserPhotoSerializer, TripSerializer, DriverLocationSerializer
from .models import Notification, Waybill, Trip, DriverLocation
from logistics.models import Task, Expense, Vehicle
from rest_framework import status

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Обновление профиля текущего пользователя"""
    serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_profile_photo(request):
    """Загрузка фото профиля"""
    serializer = UserPhotoSerializer(request.user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile_stats(request):
    """Получение статистики для профиля пользователя"""
    user = request.user
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Базовая статистика
    stats = {
        'tasks': {
            'total': Task.objects.filter(assigned_to=user).count(),
            'new': Task.objects.filter(assigned_to=user, status='NEW').count(),
            'in_progress': Task.objects.filter(assigned_to=user, status='IN_PROGRESS').count(),
            'completed': Task.objects.filter(assigned_to=user, status='COMPLETED').count()
        },
        'notifications': {
            'total': Notification.objects.filter(user=user).count(),
            'unread': Notification.objects.filter(user=user, read=False).count(),
            'today': Notification.objects.filter(
                user=user,
                created_at__gte=today
            ).count()
        }
    }
    
    # Статистика для водителей
    if user.role == 'DRIVER':
        stats['waybills'] = {
            'total': Waybill.objects.filter(driver=user).count(),
            'today': Waybill.objects.filter(driver=user, date=today).count(),
            'week': Waybill.objects.filter(driver=user, date__gte=week_ago).count(),
            'month': Waybill.objects.filter(driver=user, date__gte=month_ago).count()
        }
    
    # Статистика для бухгалтеров и снабженцев
    if user.role in ['ACCOUNTANT', 'SUPPLIER']:
        stats['expenses'] = {
            'total': Expense.objects.filter(created_by=user).count(),
            'pending': Expense.objects.filter(created_by=user, status='PENDING').count(),
            'approved': Expense.objects.filter(created_by=user, status='APPROVED').count(),
            'rejected': Expense.objects.filter(created_by=user, status='REJECTED').count()
        }
    
    return Response(stats) 

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def trips_api(request, pk=None):
    """Получить список поездок, создать новую или удалить"""
    user = request.user
    if request.method == 'GET':
        if user.role in ['SUPERADMIN', 'DIRECTOR', 'ADMIN'] or user.is_superuser:
            trips = Trip.objects.all().order_by('-date')
        else:
            trips = Trip.objects.filter(driver=user).order_by('-date')
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Проверяем права на создание поездок
        if not (user.role in ['SUPERADMIN', 'ADMIN'] or user.is_superuser):
            return Response({'detail': 'У вас нет прав для создания поездок'}, status=status.HTTP_403_FORBIDDEN)
        serializer = TripSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        # Ожидаем trips_api(request, pk=...)
        trip_id = pk or request.GET.get('id') or request.data.get('id')
        if not trip_id:
            return Response({'detail': 'Не указан id поездки'}, status=400)
        try:
            trip = Trip.objects.get(id=trip_id)
        except Trip.DoesNotExist:
            return Response({'detail': 'Поездка не найдена'}, status=404)
        # Только админ или водитель своей поездки
        if not (user.is_superuser or user.role in ['SUPERADMIN', 'ADMIN'] or trip.driver == user):
            return Response({'detail': 'Нет прав на удаление'}, status=403)
        trip.delete()
        return Response({'detail': 'Поездка удалена'})

@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([CsrfExemptSessionAuthentication])
@permission_classes([IsAuthenticated])
def driver_locations_api(request):
    """Получить историю геолокаций или отправить новую точку (оптимизированная версия)"""
    user = request.user
    
    if request.method == 'GET':
        # Временно отключаем кеширование для избежания ошибок
        # cache_key = f'driver_locations_{user.id}_{user.role}'
        # cached_data = cache.get(cache_key)
        
        # if cached_data is not None:
        #     return Response(cached_data)
        
        # Оптимизированный запрос с select_related для уменьшения количества SQL запросов
        if user.role in ['SUPERADMIN', 'ADMIN'] or user.is_superuser:
            # Для админов - показываем только последние локации каждого водителя (последние 30 минут)
            thirty_minutes_ago = timezone.now() - timedelta(minutes=30)
            all_locations = DriverLocation.objects.select_related('driver').filter(
                timestamp__gte=thirty_minutes_ago
            ).order_by('driver_id', '-timestamp')
            
            # Группируем по водителю и берем последнюю локацию для каждого (совместимо с SQLite)
            driver_latest = {}
            for location in all_locations:
                if location.driver_id not in driver_latest:
                    driver_latest[location.driver_id] = location
            
            locations = list(driver_latest.values())[:20]
        else:
            # Для водителей - только их собственные локации за последний час
            one_hour_ago = timezone.now() - timedelta(hours=1)
            locations = DriverLocation.objects.select_related('driver').filter(
                driver=user,
                timestamp__gte=one_hour_ago
            ).order_by('-timestamp')[:10]
        
        serializer = DriverLocationSerializer(locations, many=True)
        
        # Кэшируем на 2 секунды (временно отключено)
        # cache.set(cache_key, serializer.data, 2)
        
        return Response(serializer.data)
        
    elif request.method == 'POST':
        # Проверяем, что пользователь - водитель
        if user.role != 'DRIVER':
            return Response({
                'detail': f'Только водители могут отправлять локации. Ваша роль: {user.role}'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Оптимизированное создание локации
        data = request.data.copy()
        data['driver'] = user.id
        
        print(f"[DEBUG] Creating location for driver {user.username} (ID: {user.id})")
        print(f"[DEBUG] Location data: {data}")
        
        # Используем транзакцию для быстрой записи
        with transaction.atomic():
            serializer = DriverLocationSerializer(data=data)
            if serializer.is_valid():
                location = serializer.save()
                print(f"[DEBUG] Location saved successfully: {location.id}")
                # Очищаем кэш для мгновенного обновления (временно отключено)
                # cache.clear()  # Очищаем весь кэш для простоты
                # Возвращаем созданную локацию с данными водителя
                response_serializer = DriverLocationSerializer(location)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(f"[DEBUG] Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=400) 