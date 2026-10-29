from rest_framework import serializers
from .models import DataCenter, Server


class DataCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataCenter
        fields = ["id", "name", "country", "city"]


class ServerSerializer(serializers.ModelSerializer):
    datacenter_name = serializers.CharField(source="datacenter.name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Server
        fields = [
            "id", "datacenter", "datacenter_name", "name", "cpu", "ram",
            "storage", "bandwidth", "ip_address", "price", "status",
            "status_display", "description", "created_at"
        ]
        read_only_fields = ["created_at"]