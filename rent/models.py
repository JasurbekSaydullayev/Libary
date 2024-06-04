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
    from user.models import RentalUser
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rents', null=True, blank=True)
    rental_user = models.ForeignKey(RentalUser, on_delete=models.CASCADE, related_name='rents', null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='rents')
    rent_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField()
    daily_rate = models.IntegerField()
    fine_per_day = models.FloatField(default=0.01)
    status = models.CharField(max_length=20, choices=BookRentStatus, default="Kitob berilgan")
    rent_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    finally_price = models.FloatField(default=0)

    def __str__(self):
        return f'{self.user.username} rented {self.book.title}'

    def calculate_total_rent_cost(self):
        current_time = timezone.now()
        rent_date = self.rent_date.astimezone(pytz.utc)
        day_of_rent = (current_time - rent_date).days
        if day_of_rent > 0:
            day_of_rent -= 1
        self.rent_price = day_of_rent * self.book.price
        return self.rent_price

    def calculate_total_fine(self):
        current_time = timezone.now()
        rent_date = self.rent_date.astimezone(pytz.utc)
        day_of_rent = (current_time - rent_date).days
        if day_of_rent > 0:
            day_of_rent -= 1
        if self.daily_rate > day_of_rent:
            self.finally_price = self.rent_price
        else:
            self.finally_price = self.rent_price + (self.fine_per_day * self.rent_price * (day_of_rent - self.daily_rate))
        return self.finally_price
