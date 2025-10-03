from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.task import TaskViewSet, TaskFileViewSet
from .views.map import MapViewSet
from .views.vehicle import VehicleViewSet
from .views.finance import FinanceViewSet
from .views.expense import ExpenseViewSet
from .views.waybill import WaybillDocumentViewSet
# from .views.web import vehicle_detail_view, vehicle_trips_api, vehicle_gps_api
from core.views import PublicNotificationViewSet
from .api import (
    vehicle_gps_status, vehicle_gps_history, sync_vehicle_gps,
    available_gps_devices, update_all_vehicles_gps, vehicles_with_gps,
    sync_all_gps_wialon, vehicles_locations
)

app_name = 'logistics'

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'task-files', TaskFileViewSet, basename='task-file')
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'waybills', WaybillDocumentViewSet, basename='waybill')
router.register(r'map', MapViewSet, basename='map')
router.register(r'finance', FinanceViewSet, basename='finance')
router.register(r'public-notifications', PublicNotificationViewSet, basename='public-notification')

urlpatterns = [
    path('', include(router.urls)),
    path('map/live_tracking/', MapViewSet.as_view({'get': 'get_vehicles'}), name='live-tracking'),
    path('map/update_location/', MapViewSet.as_view({'post': 'update_location'}), name='update-location'),
    path('map/tracking_status/', MapViewSet.as_view({'post': 'update_tracking_status'}), name='tracking-status'),
    
    # GPS мониторинг API
    path('gps/vehicles/<int:vehicle_id>/status/', vehicle_gps_status, name='vehicle-gps-status'),
    path('gps/vehicles/<int:vehicle_id>/history/', vehicle_gps_history, name='vehicle-gps-history'),
    path('gps/vehicles/<int:vehicle_id>/sync/', sync_vehicle_gps, name='sync-vehicle-gps'),
    path('gps/devices/available/', available_gps_devices, name='available-gps-devices'),
    path('gps/vehicles/update-all/', update_all_vehicles_gps, name='update-all-vehicles-gps'),
    path('gps/wialon/sync-all/', sync_all_gps_wialon, name='sync-all-gps-wialon'),
    path('gps/vehicles/with-gps/', vehicles_with_gps, name='vehicles-with-gps'),
    path('gps/vehicles/locations/', vehicles_locations, name='vehicles-locations'),
    
    # Веб-страницы
    # path('vehicles/<int:vehicle_id>/', vehicle_detail_view, name='vehicle-detail'),
    # path('vehicle-trips/<int:vehicle_id>/', vehicle_trips_api, name='vehicle-trips-api'),
    # path('vehicle-gps/<int:vehicle_id>/', vehicle_gps_api, name='vehicle-gps-api'),
] 