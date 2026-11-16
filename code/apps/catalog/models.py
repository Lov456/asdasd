from django.db import models


class DataCenter(models.Model):
    """Склад / Помещение хранения компьютерной техники."""
    name = models.CharField("Название склада / кабинета", max_length=100, unique=True)
    country = models.CharField("Корпус / Здание", max_length=50, default="Главный корпус")
    city = models.CharField("Этаж / Секция", max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады и помещения"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.city or self.country})"


class Server(models.Model):
    """Единица компьютерной техники на складе."""
    class Status(models.TextChoices):
        AVAILABLE = "available", "На складе (в наличии)"
        RESERVED = "reserved", "Зарезервировано"
        RENTED = "rented", "Выдано в эксплуатацию"
        MAINTENANCE = "maintenance", "В ремонте / Списано"

    datacenter = models.ForeignKey(
        DataCenter,
        on_delete=models.PROTECT,
        related_name="servers",
        verbose_name="Склад хранения",
    )
    name = models.CharField("Модель / Наименование ПК", max_length=100)
    cpu = models.CharField("Процессор", max_length=100, blank=True)
    ram = models.PositiveIntegerField("ОЗУ, ГБ", default=8)
    storage = models.CharField("Накопители (SSD/HDD)", max_length=100, blank=True)
    bandwidth = models.PositiveIntegerField("Количество (шт.)", default=1)
    ip_address = models.CharField("Инвентарный / Серийный номер", max_length=50, unique=True, null=True, blank=True)
    price = models.DecimalField("Балансовая стоимость, ₽", max_digits=12, decimal_places=2, default=0)
    status = models.CharField(
        "Статус", max_length=20, choices=Status.choices, default=Status.AVAILABLE
    )
    description = models.TextField("Комплектация / Примечания", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Компьютерная техника"
        verbose_name_plural = "Компьютерная техника"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} [Инв. № {self.ip_address or 'б/н'}] ({self.datacenter.name})"

    @property
    def is_available(self):
        return self.status == self.Status.AVAILABLE