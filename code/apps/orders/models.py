from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.catalog.models import Server
from apps.clients.models import Client


class Order(models.Model):
    """Заказ на аренду сервера или инфраструктурные услуги."""
    class OrderType(models.TextChoices):
        RENT = "rent", "Аренда сервера"
        SETUP = "setup", "Настройка и администрирование"
        EXTRA_IP = "extra_ip", "Дополнительные IP / Канал"

    class Status(models.TextChoices):
        NEW = "new", "Новый"
        CONFIRMED = "confirmed", "Подтверждён"
        COMPLETED = "completed", "Активен / Завершён"
        CANCELLED = "cancelled", "Отменён"

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="orders", verbose_name="Клиент"
    )
    server = models.ForeignKey(
        Server, on_delete=models.PROTECT, related_name="orders", verbose_name="Сервер"
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders", verbose_name="Менеджер"
    )
    order_type = models.CharField("Тип услуги", max_length=20, choices=OrderType.choices, default=OrderType.RENT)
    total_amount = models.DecimalField("Сумма к оплате, ₽", max_digits=12, decimal_places=2, default=0)
    status = models.CharField("Статус", max_length=20, choices=Status.choices, default=Status.NEW)
    comment = models.TextField("Комментарий / Конфиг ОС", blank=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    completed_at = models.DateTimeField("Активирован", null=True, blank=True)

    class Meta:
        verbose_name = "Заказ на аренду"
        verbose_name_plural = "Заказы на аренду"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заказ #{self.pk} — {self.client.full_name} ({self.server.name})"

    def save(self, *args, **kwargs):
        """Резервирование сервера при создании заказа."""
        if not self.pk and self.order_type == self.OrderType.RENT:
            if self.server.status == Server.Status.AVAILABLE:
                self.server.status = Server.Status.RESERVED
                self.server.save()
        super().save(*args, **kwargs)

    def complete(self):
        """Активация аренды."""
        self.status = self.Status.COMPLETED
        self.completed_at = timezone.now()
        if self.order_type == self.OrderType.RENT:
            self.server.status = Server.Status.RENTED
            self.server.save()
        self.save()

    def cancel(self):
        """Отмена заказа и освобождение сервера."""
        self.status = self.Status.CANCELLED
        if self.server.status == Server.Status.RESERVED:
            self.server.status = Server.Status.AVAILABLE
            self.server.save()
        self.save()