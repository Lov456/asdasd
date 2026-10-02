from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Админка Django
    path("admin/", admin.site.urls),
    # МОДУЛЬ 1: АВТОРИЗАЦИЯ
    path("api/auth/", include("apps.accounts.urls")),
    # МОДУЛЬ 2: КАТАЛОГ
    path("api/", include("apps.catalog.urls")),
    # МОДУЛЬ 3: КЛИЕНТЫ
    path("api/clients/", include("apps.clients.urls")),
    # МОДУЛЬ 4: ЗАКАЗЫ
    path("api/orders/", include("apps.orders.urls")),
    # МОДУЛЬ 5: ОТЧЕТЫ
    path("api/reports/", include("apps.reports.urls")),
    # DRF-вход через браузер
    path("api/drf-login/", include("rest_framework.urls")),
]