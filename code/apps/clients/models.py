from django.db import models
from django.conf import settings


class Client(models.Model):
    """Отдел / Сотрудник — получатель компьютерной техники."""
    full_name = models.CharField("ФИО сотрудника / Название отдела", max_length=150)
    phone = models.CharField("Внутренний / Рабочий телефон", max_length=20, unique=True)
    email = models.EmailField("Корпоративный Email", unique=True)
    telegram = models.CharField("Кабинет / Рабочее место", max_length=50, blank=True)
    billing_id = models.CharField("Табельный номер / Код отдела", max_length=30, blank=True)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clients",
        verbose_name="Ответственный кладовщик",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Получатель / Отдел"
        verbose_name_plural = "Получатели и отделы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} ({self.telegram or self.email})"