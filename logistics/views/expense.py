from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncDate, TruncMonth
from datetime import datetime, timedelta
from ..models import Expense, Vehicle
from ..serializers import ExpenseSerializer, ExpenseReportSerializer
from .base import BaseModelViewSet

class ExpenseViewSet(BaseModelViewSet):
    queryset = Expense.objects.all().select_related('created_by', 'vehicle').order_by('-created_at')
    serializer_class = ExpenseSerializer
    filterset_fields = ['category', 'vehicle', 'created_by', 'date']
    search_fields = ['description', 'vehicle__number', 'created_by__first_name', 'created_by__last_name']
    ordering_fields = ['date', 'amount', 'created_at']
    
    def get_permissions(self):
        """
        Разрешения по ролям:
        - Водители, диспетчеры, снабженцы: могут создавать и просматривать свои расходы
        - Бухгалтеры, директора, админы: могут просматривать все расходы и отчеты
        """
        if self.action in ['create']:
            # Создавать расходы могут: водители, диспетчеры, снабженцы
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['list', 'retrieve']:
            # Просматривать могут все авторизованные
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Редактировать/удалять могут только создатели или админы
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def filter_queryset_by_role(self, queryset):
        """Фильтрация по ролям пользователей"""
        user = self.request.user
        
        # Админы, директора, бухгалтеры видят все расходы
        if user.role in ['SUPERADMIN', 'ADMIN', 'DIRECTOR', 'ACCOUNTANT'] or user.is_superuser:
            return queryset
        
        # Водители, диспетчеры, снабженцы видят только свои расходы
        elif user.role in ['DRIVER', 'DISPATCHER', 'SUPPLIER']:
            return queryset.filter(created_by=user)
        
        # Остальные роли не видят расходы
        return queryset.none()
    
    def perform_create(self, serializer):
        """Создание расхода с проверкой прав"""
        user = self.request.user
        
        # Проверяем, может ли пользователь создавать расходы
        if user.role not in ['DRIVER', 'DISPATCHER', 'SUPPLIER', 'SUPERADMIN', 'ADMIN']:
            raise PermissionError('У вас нет прав для создания расходов')
        
        serializer.save(created_by=user)
    
    def update(self, request, *args, **kwargs):
        """Обновление расхода с проверкой прав"""
        instance = self.get_object()
        user = request.user
        
        # Редактировать могут только создатели или админы
        if instance.created_by != user and user.role not in ['SUPERADMIN', 'ADMIN'] and not user.is_superuser:
            return Response(
                {'detail': 'У вас нет прав для редактирования этого расхода'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Удаление расхода с проверкой прав"""
        instance = self.get_object()
        user = request.user
        
        # Удалять могут только создатели или админы
        if instance.created_by != user and user.role not in ['SUPERADMIN', 'ADMIN'] and not user.is_superuser:
            return Response(
                {'detail': 'У вас нет прав для удаления этого расхода'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def my_expenses(self, request):
        """Получить расходы текущего пользователя"""
        queryset = self.get_queryset().filter(created_by=request.user)
        
        # Фильтрация по датам
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def report(self, request):
        """Отчет по расходам (только для бухгалтеров, директоров, админов)"""
        user = request.user
        
        if user.role not in ['SUPERADMIN', 'ADMIN', 'DIRECTOR', 'ACCOUNTANT'] and not user.is_superuser:
            return Response(
                {'detail': 'У вас нет прав для просмотра отчетов'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        vehicle_id = request.query_params.get('vehicle_id')
        user_id = request.query_params.get('user_id')
        
        queryset = self.get_queryset()
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if vehicle_id:
            queryset = queryset.filter(vehicle_id=vehicle_id)
        if user_id:
            queryset = queryset.filter(created_by_id=user_id)
        
        # Отчет по категориям
        report_by_category = queryset.values('category').annotate(
            total_amount=Sum('amount'),
            count=Count('id')
        ).order_by('-total_amount')
        
        # Общая сумма
        total_amount = queryset.aggregate(total=Sum('amount'))['total'] or 0
        
        # Отчет по пользователям
        report_by_user = queryset.values(
            'created_by__id',
            'created_by__first_name', 
            'created_by__last_name'
        ).annotate(
            total_amount=Sum('amount'),
            count=Count('id')
        ).order_by('-total_amount')
        
        # Отчет по дням
        report_by_day = queryset.annotate(
            day=TruncDate('date')
        ).values('day').annotate(
            total_amount=Sum('amount'),
            count=Count('id')
        ).order_by('-day')[:30]  # Последние 30 дней
        
        return Response({
            'total_amount': total_amount,
            'by_category': list(report_by_category),
            'by_user': list(report_by_user),
            'by_day': list(report_by_day),
            'period': {
                'start_date': start_date,
                'end_date': end_date
            }
        })
    
    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        """Месячная сводка по расходам"""
        user = request.user
        
        if user.role not in ['SUPERADMIN', 'ADMIN', 'DIRECTOR', 'ACCOUNTANT'] and not user.is_superuser:
            return Response(
                {'detail': 'У вас нет прав для просмотра сводок'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        months = int(request.query_params.get('months', 6))
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30 * months)
        
        monthly_data = self.get_queryset().filter(
            date__gte=start_date,
            date__lte=end_date
        ).annotate(
            month=TruncMonth('date')
        ).values('month').annotate(
            total_amount=Sum('amount'),
            count=Count('id')
        ).order_by('month')
        
        return Response(list(monthly_data))
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Получить список категорий расходов"""
        categories = [
            {'value': choice[0], 'label': choice[1]} 
            for choice in Expense.Category.choices
        ]
        return Response(categories)
    
    @action(detail=False, methods=['get'])
    def vehicles_for_expenses(self, request):
        """Получить список транспорта для выбора в расходах"""
        vehicles = Vehicle.objects.filter(is_archived=False).values(
            'id', 'number', 'brand', 'model'
        ).order_by('number')
        return Response(list(vehicles)) 