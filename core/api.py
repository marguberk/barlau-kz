from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from .serializers import UserUpdateSerializer, UserPhotoSerializer, TripSerializer, DriverLocationSerializer
from .models import Notification, Waybill, Trip, DriverLocation
from logistics.models import Task, Expense, Vehicle
from rest_framework import status

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

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def trips_api(request):
    """Получить список поездок или создать новую"""
    user = request.user
    if request.method == 'GET':
        if user.role in ['DIRECTOR', 'SUPERADMIN', 'ADMIN'] or user.is_superuser:
            trips = Trip.objects.all().order_by('-date')
        else:
            trips = Trip.objects.filter(driver=user).order_by('-date')
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TripSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def driver_locations_api(request):
    """Получить историю геолокаций или отправить новую точку"""
    user = request.user
    if request.method == 'GET':
        if user.role in ['DIRECTOR', 'SUPERADMIN', 'ADMIN'] or user.is_superuser:
            locations = DriverLocation.objects.all().order_by('-timestamp')
        else:
            locations = DriverLocation.objects.filter(driver=user).order_by('-timestamp')
        serializer = DriverLocationSerializer(locations, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data.copy()
        data['driver'] = user.id
        serializer = DriverLocationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400) 