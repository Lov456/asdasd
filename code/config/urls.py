from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

# Настройка заголовков системы под тему складского учёта
admin.site.site_header = "Складской учёт компьютерной техники"
admin.site.site_title = "Учёт КТ | Панель управления"
admin.site.index_title = "Управление складом и движением техники"

urlpatterns = [
    # Автоматический переход с главной страницы в панель управления
    path("", RedirectView.as_view(url="/admin/", permanent=False)),
    # Панель управления (Админка)
    path("admin/", admin.site.urls),
    # МОДУЛЬ 1: АВТОРИЗАЦИЯ
    path("api/auth/", include("apps.accounts.urls")),
    # МОДУЛЬ 2: КАТАЛОГ ТЕХНИКИ И СКЛАДОВ
    path("api/", include("apps.catalog.urls")),
    # МОДУЛЬ 3: ПОЛУЧАТЕЛИ И ОТДЕЛЫ
    path("api/clients/", include("apps.clients.urls")),
    # МОДУЛЬ 4: СКЛАДСКИЕ ОПЕРАЦИИ (НАКЛАДНЫЕ)
    path("api/orders/", include("apps.orders.urls")),
    # МОДУЛЬ 5: ОТЧЕТЫ
    path("api/reports/", include("apps.reports.urls")),
    # DRF-вход через браузер
    path("api/drf-login/", include("rest_framework.urls")),
]