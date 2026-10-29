from datetime import timedelta
from django.db.models import Count, Sum
from django.utils import timezone
from apps.catalog.models import Server
from apps.orders.models import Order


class ReportService:
    """Сервис аналитики серверной инфраструктуры."""

    @staticmethod
    def kpi(days: int = 30) -> dict:
        """Ключевые показатели бизнеса."""
        since = timezone.now() - timedelta(days=days)
        completed = Order.objects.filter(
            order_type=Order.OrderType.RENT,
            status=Order.Status.COMPLETED,
            created_at__gte=since,
        )
        revenue = completed.aggregate(total=Sum("total_amount"))["total"] or 0
        count = completed.count()
        return {
            "revenue": float(revenue),
            "sales_count": count,
            "avg_check": float(revenue) / count if count else 0,
            "in_stock": Server.objects.filter(status=Server.Status.AVAILABLE).count(),
            "period_days": days,
        }

    @staticmethod
    def revenue_by_day(days: int = 30) -> list:
        """Динамика выручки по дням."""
        since = timezone.now() - timedelta(days=days)
        rows = (
            Order.objects.filter(
                order_type=Order.OrderType.RENT,
                status=Order.Status.COMPLETED,
                created_at__gte=since,
            )
            .extra(select={"day": "DATE(created_at)"})
            .values("day")
            .annotate(total=Sum("total_amount"))
            .order_by("day")
        )
        return [{"date": str(r["day"]), "total": float(r["total"])} for r in rows]

    @staticmethod
    def top_models(limit: int = 5) -> list:
        """Топ популярных тарифов / серверов."""
        rows = (
            Order.objects.filter(
                order_type=Order.OrderType.RENT,
                status=Order.Status.COMPLETED,
            )
            .values("server__datacenter__name", "server__name")
            .annotate(count=Count("id"))
            .order_by("-count")[:limit]
        )
        return [
            {"brand": r["server__datacenter__name"], "model": r["server__name"], "count": r["count"]}
            for r in rows
        ]

    @staticmethod
    def manager_load(days: int = 30) -> list:
        """Загрузка менеджеров по заключенным договорам."""
        since = timezone.now() - timedelta(days=days)
        rows = (
            Order.objects.filter(
                order_type=Order.OrderType.RENT,
                created_at__gte=since,
            )
            .values("manager__username")
            .annotate(count=Count("id"), total=Sum("total_amount"))
        )
        return [
            {"manager": r["manager__username"], "orders": r["count"], "total": float(r["total"] or 0)}
            for r in rows
        ]

    @staticmethod
    def stock_status() -> list:
        """Состояние серверного парка."""
        return [
            {"status": r["status"], "count": r["count"]}
            for r in Server.objects.values("status").annotate(count=Count("id"))
        ]