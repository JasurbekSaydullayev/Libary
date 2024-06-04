from django.contrib import admin

from .models import BookRent, BookReservation


@admin.register(BookRent)
class BookRentAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'status')


@admin.register(BookReservation)
class BookReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'is_active', 'is_confirmed')
    list_editable = ('is_active', 'is_confirmed')
