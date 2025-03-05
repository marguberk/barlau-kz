from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from .serializers import UserUpdateSerializer, UserPhotoSerializer
from .models import Notification, Waybill
from logistics.models import Task, Expense

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
            'unread': Notification.objects.filter(user=user, is_read=False).count(),
            'today': Notification.objects.filter(
                user=user,
                created_at__date=today
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