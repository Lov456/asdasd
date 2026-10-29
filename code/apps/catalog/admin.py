from django.contrib import admin
from .models import DataCenter, Server


@admin.register(DataCenter)
class DataCenterAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "city", "created_at")
    search_fields = ("name", "country", "city")


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ("name", "datacenter", "cpu", "ram", "ip_address", "price", "status")
    list_filter = ("datacenter", "status")
    search_fields = ("name", "cpu", "ip_address")
    list_editable = ("status",)