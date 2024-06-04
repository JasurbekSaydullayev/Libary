from django.db import models
from django.contrib.auth import get_user_model
from books.models import Book
from django.utils import timezone
import pytz

User = get_user_model()


class BookReservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reservations')
    reservation_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
    days = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} reserved {self.book.title}'


BookRentStatus = (
    ("Kitob berilgan", "Kitob berilgan"),
    ("Kitob qaytarilgan", "Kitob qaytarilgan"),
)


class BookRent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rents')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='rents')
    rent_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    daily_rate = models.IntegerField()
    fine_per_day = models.FloatField(default=0.01)
    status = models.CharField(max_length=20, choices=BookRentStatus, default="Kitob berilgan")
    finaly_price = models.FloatField(default=0)

    def __str__(self):
        return f'{self.user.username} rented {self.book.title}'

    def calculate_total_rent_cost(self):
        current_time = timezone.now()
        rent_date = self.rent_date.astimezone(pytz.utc)
        if self.return_date:
            return_date = self.return_date.astimezone(pytz.utc)
            duration = (return_date - rent_date).days
        else:
            duration = (current_time - rent_date).days
        return self.daily_rate * duration

    def calculate_total_fine(self):
        if not self.return_date:
            return 0
        rent_date = self.rent_date.astimezone(pytz.utc)
        return_date = self.return_date.astimezone(pytz.utc)
        duration = (return_date - rent_date).days
        book_cost = self.book.price
        if duration <= 0:
            return 0
        if duration > self.daily_rate:
            total_fine = (self.daily_rate * book_cost) + (book_cost * self.fine_per_day * (duration - self.daily_rate))
        elif duration < self.daily_rate:
            total_fine = (self.daily_rate - duration) * book_cost
        return total_fine
