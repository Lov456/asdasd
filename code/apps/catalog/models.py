from django.db import models


class DataCenter(models.Model):
    """Дата-центр / Локация размещения."""
    name = models.CharField("Название ДЦ", max_length=100, unique=True)
    country = models.CharField("Страна", max_length=50)
    city = models.CharField("Город", max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Дата-центр"
        verbose_name_plural = "Дата-центры"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.city or self.country})"


class Server(models.Model):
    """Выделенный или виртуальный сервер."""
    class Status(models.TextChoices):
        AVAILABLE = "available", "Свободен"
        RESERVED = "reserved", "Забронирован"
        RENTED = "rented", "Арендован"
        MAINTENANCE = "maintenance", "Техобслуживание"

    datacenter = models.ForeignKey(
        DataCenter,
        on_delete=models.PROTECT,
        related_name="servers",
        verbose_name="Дата-центр",
    )
    name = models.CharField("Имя/Тариф", max_length=100)
    cpu = models.CharField("Процессор", max_length=100)
    ram = models.PositiveIntegerField("ОЗУ, ГБ")
    storage = models.CharField("Накопители", max_length=100)
    bandwidth = models.PositiveIntegerField("Канал, Мбит/с", default=1000)
    ip_address = models.GenericIPAddressField("Выделенный IP", protocol="IPv4", unique=True, null=True, blank=True)
    price = models.DecimalField("Аренда в мес., ₽", max_digits=12, decimal_places=2)
    status = models.CharField(
        "Статус", max_length=20, choices=Status.choices, default=Status.AVAILABLE
    )
    description = models.TextField("Описание / Примечания", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Сервер"
        verbose_name_plural = "Серверы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} [{self.cpu} / {self.ram}GB RAM] ({self.datacenter.name})"

    @property
    def is_available(self):
        return self.status == self.Status.AVAILABLE