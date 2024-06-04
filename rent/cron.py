from django.utils import timezone
from rent.models import BookReservation


def bron_cancel():
    try:
        one_day_ago = timezone.now() - timezone.timedelta(days=1)
        expired_reservations = BookReservation.objects.filter(
            is_active=True, reservation_date__gt=one_day_ago
        )
        for reservation in expired_reservations:
            reservation.is_active = False
            reservation.save()
        print("Eskirgan bronlar bekor qilindi")

    except Exception as e:
        print("Hatolik", e)