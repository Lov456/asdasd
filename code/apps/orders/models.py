from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.catalog.models import Server
from apps.clients.models import Client


class Order(models.Model):
    """Складская операция (накладная / акт приёма-передачи техники)."""
    class OrderType(models.TextChoices):
        RENT = "rent", "Выдача в эксплуатацию"
        SETUP = "setup", "Ввод в эксплуатацию / Настройка"
        EXTRA_IP = "extra_ip", "Модернизация / Замена комплектующих"

    class Status(models.TextChoices):
        NEW = "new", "Черновик (оформляется)"
        CONFIRMED = "confirmed", "Утверждена руководителем"
        COMPLETED = "completed", "Проведена (техника выдана)"
        CANCELLED = "cancelled", "Отменена / Возврат на склад"

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="orders", verbose_name="Получатель / Отдел"
    )
    server = models.ForeignKey(
        Server, on_delete=models.PROTECT, related_name="orders", verbose_name="Компьютерная техника"
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders", verbose_name="Кладовщик"
    )
    order_type = models.CharField("Тип операции", max_length=20, choices=OrderType.choices, default=OrderType.RENT)
    total_amount = models.DecimalField("Балансовая стоимость по акту, ₽", max_digits=12, decimal_places=2, default=0)
    status = models.CharField("Статус накладной", max_length=20, choices=Status.choices, default=Status.NEW)
    comment = models.TextField("Примечание / Установленное ПО", blank=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    completed_at = models.DateTimeField("Дата выдачи", null=True, blank=True)

    class Meta:
        verbose_name = "Складская операция"
        verbose_name_plural = "Складские операции (накладные)"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Накладная #{self.pk} — {self.client.full_name} ({self.server.name})"

    def save(self, *args, **kwargs):
        """Резервирование техники на складе при создании накладной на выдачу."""
        if not self.pk and self.order_type == self.OrderType.RENT:
            if self.server.status == Server.Status.AVAILABLE:
                self.server.status = Server.Status.RESERVED
                self.server.save()
        super().save(*args, **kwargs)

    def complete(self):
        """Проведение накладной и выдача техники в эксплуатацию."""
        self.status = self.Status.COMPLETED
        self.completed_at = timezone.now()
        if self.order_type == self.OrderType.RENT:
            self.server.status = Server.Status.RENTED
            self.server.save()
        self.save()

    def cancel(self):
        """Отмена накладной и возврат техники на склад."""
        self.status = self.Status.CANCELLED
        if self.server.status == Server.Status.RESERVED:
            self.server.status = Server.Status.AVAILABLE
            self.server.save()
        self.save()