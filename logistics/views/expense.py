from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from ..models import Expense
from ..serializers import ExpenseSerializer, ExpenseReportSerializer
from .base import BaseModelViewSet

class ExpenseViewSet(BaseModelViewSet):
    queryset = Expense.objects.all().order_by('-date')
    serializer_class = ExpenseSerializer
    filterset_fields = ['category', 'vehicle', 'created_by', 'date']
    
    def filter_queryset_by_role(self, queryset):
        if self.request.user.role == 'ACCOUNTANT':
            return queryset
        elif self.request.user.role == 'SUPPLIER':
            return queryset.filter(created_by=self.request.user)
        return queryset
    
    @action(detail=False, methods=['get'])
    def report(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        queryset = self.get_queryset()
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        report = queryset.values('category').annotate(
            total_amount=Sum('amount'),
            count=Count('id')
        )
        
        serializer = ExpenseReportSerializer(report, many=True)
        return Response(serializer.data) 