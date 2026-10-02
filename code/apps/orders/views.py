from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """CRUD для заказов с экшенами complete / cancel."""
    queryset = Order.objects.select_related("client", "car", "manager").all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "order_type", "manager"]
    search_fields = ["client__full_name", "car__model"]
    ordering_fields = ["created_at", "total_amount"]

    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        order = self.get_object()
        order.complete()
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        order = self.get_object()
        order.cancel()
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)