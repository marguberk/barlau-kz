from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TaskViewSet,
    VehicleViewSet,
    ExpenseViewSet,
    WaybillDocumentViewSet,
    MapViewSet,
    FinanceViewSet
)

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'waybills', WaybillDocumentViewSet, basename='waybill')
router.register(r'map', MapViewSet, basename='map')
router.register(r'finance', FinanceViewSet, basename='finance')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
] 