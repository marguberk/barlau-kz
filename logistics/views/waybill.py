from ..models import WaybillDocument
from ..serializers import WaybillDocumentSerializer
from .base import BaseModelViewSet

class WaybillDocumentViewSet(BaseModelViewSet):
    queryset = WaybillDocument.objects.all().order_by('-date')
    serializer_class = WaybillDocumentSerializer
    filterset_fields = ['driver', 'vehicle', 'date']
    
    def filter_queryset_by_role(self, queryset):
        if self.request.user.role == 'DRIVER':
            return queryset.filter(driver=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user) 