from rest_framework import viewsets
from blog.Models.AuditLogModel import AuditLog
from blog.Serializers.AuditLogSerializer import AuditLogSerializer

class AuditLogViewSet(viewsets.ModelViewSet):
    serializer_class = AuditLogSerializer
    queryset = AuditLog.objects.all()
    