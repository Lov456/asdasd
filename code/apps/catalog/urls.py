from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DataCenterViewSet, ServerViewSet

router = DefaultRouter()
router.register("datacenters", DataCenterViewSet, basename="datacenters")
router.register("servers", ServerViewSet, basename="servers")

urlpatterns = [
    path("", include(router.urls)),
]