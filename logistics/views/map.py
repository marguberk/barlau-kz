from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from ..models import Vehicle, Task
from ..serializers import VehicleLocationSerializer, TaskLocationSerializer

class MapViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        """Получить все данные для карты"""
        vehicles = self.get_vehicles(request)
        tasks = self.get_tasks(request)
        
        return Response({
            'vehicles': vehicles.data,
            'tasks': tasks.data
        })
    
    def get_vehicles(self, request):
        """Получить местоположение всех транспортных средств"""
        vehicles = Vehicle.objects.filter(
            driver__isnull=False,
            driver__current_latitude__isnull=False,
            driver__current_longitude__isnull=False
        ).order_by('number')
        
        if request.user.role == 'DRIVER':
            vehicles = vehicles.filter(driver=request.user)
            
        serializer = VehicleLocationSerializer(vehicles, many=True)
        return Response(serializer.data)
    
    def get_tasks(self, request):
        """Получить местоположение всех активных задач"""
        tasks = Task.objects.filter(
            status__in=['NEW', 'IN_PROGRESS'],
            deadline__gte=timezone.now(),
            vehicle__isnull=False,
            vehicle__driver__isnull=False,
            vehicle__driver__current_latitude__isnull=False,
            vehicle__driver__current_longitude__isnull=False
        ).order_by('-created_at')
        
        if request.user.role == 'DRIVER':
            tasks = tasks.filter(assigned_to=request.user)
            
        serializer = TaskLocationSerializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def update_location(self, request):
        """Обновить местоположение транспортного средства"""
        if not request.user.role == 'DRIVER':
            return Response(
                {"detail": "Только водители могут обновлять местоположение"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        vehicle = Vehicle.objects.filter(driver=request.user).first()
        if not vehicle:
            return Response(
                {"detail": "Транспортное средство не найдено"},
                status=status.HTTP_404_NOT_FOUND
            )
            
        request.user.current_latitude = request.data.get('latitude')
        request.user.current_longitude = request.data.get('longitude')
        request.user.last_location_update = timezone.now()
        request.user.save()
        
        serializer = VehicleLocationSerializer(vehicle)
        return Response(serializer.data) 