from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import DataCenter, Server
from .serializers import DataCenterSerializer, ServerSerializer


class DataCenterViewSet(viewsets.ModelViewSet):
    """CRUD для дата-центров."""
    queryset = DataCenter.objects.all()
    serializer_class = DataCenterSerializer
    search_fields = ["name", "country", "city"]
    filter_backends = [filters.SearchFilter]


class ServerViewSet(viewsets.ModelViewSet):
    """CRUD для серверов с фильтрацией."""
    queryset = Server.objects.select_related("datacenter").all()
    serializer_class = ServerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["datacenter", "status", "ram"]
    search_fields = ["name", "cpu", "ip_address", "datacenter__name"]
    ordering_fields = ["price", "ram", "created_at"]