from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.task import TaskViewSet
from .views.map import MapViewSet
from .views.vehicle import VehicleViewSet
from .views.finance import FinanceViewSet
from .views.expense import ExpenseViewSet
from .views.waybill import WaybillDocumentViewSet

app_name = 'logistics'

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'waybills', WaybillDocumentViewSet, basename='waybill')
router.register(r'map', MapViewSet, basename='map')
router.register(r'finance', FinanceViewSet, basename='finance')

urlpatterns = [
    path('', include(router.urls)),
    path('map/live_tracking/', MapViewSet.as_view({'get': 'get_vehicles'}), name='live-tracking'),
] 