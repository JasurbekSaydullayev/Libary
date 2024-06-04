from django.core.management.base import BaseCommand
from django.utils import timezone
from rent.models import BookReservation


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        one_day_ago = timezone.now() - timezone.timedelta(days=1)
        expired_reservations = BookReservation.objects.filter(
            is_active=True, reservation_date__lt=one_day_ago
        )
        for reservation in expired_reservations:
            reservation.is_active = False
            reservation.save()
        self.stdout.write(self.style.SUCCESS('Eskirgan bronlar bekor qilindi'))
