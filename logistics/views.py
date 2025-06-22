from .views.task import TaskViewSet, TaskFileViewSet
from .views.vehicle import VehicleViewSet
from .views.expense import ExpenseViewSet
from .views.waybill import WaybillDocumentViewSet
from .views.map import MapViewSet
from .views.employee import EmployeeViewSet
from .views.finance import FinanceViewSet
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Vehicle, Task, Expense, WaybillDocument
from .serializers import (
    VehicleSerializer, TaskSerializer, ExpenseSerializer,
    VehicleLocationSerializer, TaskLocationSerializer,
    ExpenseReportSerializer, WaybillDocumentSerializer,
    FinancialReportSerializer
)
from .filters import ExpenseFilter
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta

__all__ = [
    'TaskViewSet',
    'TaskFileViewSet',
    'VehicleViewSet',
    'ExpenseViewSet',
    'WaybillDocumentViewSet',
    'MapViewSet',
    'EmployeeViewSet',
    'FinanceViewSet'
]

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all().order_by('-date')
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ExpenseFilter
    search_fields = ['description']
    ordering_fields = ['date', 'amount']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def report(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        vehicle_id = request.query_params.get('vehicle_id')
        
        queryset = self.get_queryset()
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if vehicle_id:
            queryset = queryset.filter(vehicle_id=vehicle_id)
            
        report_data = queryset.values('category').annotate(
            total_amount=Sum('amount'),
            count=Count('id')
        ).order_by('-total_amount')
        
        serializer = ExpenseReportSerializer(report_data, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def monthly_report(self, request):
        months = int(request.query_params.get('months', 12))
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
        
        return Response(monthly_data)
