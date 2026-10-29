from django.db import models
from django.conf import settings


class Client(models.Model):
    """Клиент / Арендатор серверных мощностей."""
    full_name = models.CharField("ФИО / Организация", max_length=150)
    phone = models.CharField("Телефон", max_length=20, unique=True)
    email = models.EmailField("Email", unique=True)
    telegram = models.CharField("Telegram", max_length=50, blank=True)
    billing_id = models.CharField("Номер лицевого счёта", max_length=30, blank=True)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clients",
        verbose_name="Менеджер",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} ({self.email})"