from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from ..models import Vehicle
from ..serializers import VehicleSerializer, VehicleLocationSerializer
from .base import BaseModelViewSet

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
    permission_classes = [permissions.IsAuthenticated, IsDirectorOrReadOnly]
    filterset_class = VehicleFilter
    
    def filter_queryset_by_role(self, queryset):
        if self.request.user.role == 'DRIVER':
            return queryset.filter(driver=self.request.user)
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
        serializer.save(created_by=self.request.user) 