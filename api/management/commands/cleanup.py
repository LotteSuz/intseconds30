from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from ...models import Session


class Command(BaseCommand):
    help = "Removes session older than 6 hours"

    def handle(self, *args, **options):
        threshold = timezone.now() - timedelta(hours=6)

        sessions = Session.objects.filter(last_activity__lt=threshold)
        sessions_deleted = len(sessions)
        sessions.delete()

        if sessions_deleted > 1:
            self.stdout.write(self.style.SUCCESS(f"Removed {sessions_deleted} sessions"))
        elif sessions_deleted is 1:
            self.stdout.write(self.style.SUCCESS(f"Removed {sessions_deleted} session"))
        else:
            self.stdout.write(self.style.WARNING(f"No sessions to remove"))
