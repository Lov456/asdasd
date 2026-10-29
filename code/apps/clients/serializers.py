from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source="manager.get_full_name", read_only=True)

    class Meta:
        model = Client
        fields = [
            "id", "full_name", "phone", "email", "telegram",
            "billing_id", "manager", "manager_name", "created_at"
        ]
        read_only_fields = ["created_at"]