from ..models import WaybillDocument
from ..serializers import WaybillDocumentSerializer
from .base import BaseModelViewSet
from core.models import Notification

class WaybillDocumentViewSet(BaseModelViewSet):
    queryset = WaybillDocument.objects.all().order_by('-date')
    serializer_class = WaybillDocumentSerializer
    filterset_fields = ['driver', 'vehicle', 'date']
    
    def filter_queryset_by_role(self, queryset):
        if self.request.user.role == 'DRIVER':
            return queryset.filter(driver=self.request.user)
        return queryset

    def perform_create(self, serializer):
        waybill = serializer.save(created_by=self.request.user)
        # Уведомление для водителя
        if waybill.driver:
            Notification.create_waybill_notification(waybill.driver, waybill)
        # Уведомление для создателя, если это не водитель
        if waybill.created_by and waybill.created_by != waybill.driver:
            Notification.create_waybill_notification(waybill.created_by, waybill) 