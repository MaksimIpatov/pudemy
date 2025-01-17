import json

from django.core.management.base import BaseCommand
from django_celery_beat.models import IntervalSchedule, PeriodicTask


class Command(BaseCommand):
    help = "Периодическая задача для блокировки неактивных пользователей"

    def handle(self, *args, **kwargs) -> None:
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.DAYS,
        )
        task, created = PeriodicTask.objects.get_or_create(
            interval=schedule,
            name="Деактивация неактивных пользователей",
            task="users.tasks.deactivate_inactive_users",
            defaults={"kwargs": json.dumps({})},
        )
        self.stdout.write(
            "Задача успешно создана." if created else "Задача уже существует."
        )
