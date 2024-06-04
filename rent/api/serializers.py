from rest_framework import serializers
from ..models import BookReservation, BookRent
from datetime import datetime, timedelta


class BookReservationSerializer(serializers.ModelSerializer):
    days = serializers.IntegerField(write_only=True)
    reservation_date = serializers.DateTimeField(read_only=True, format='%m/%d/%Y %H:%M')
    expiration_date = serializers.DateTimeField(read_only=True, format='%m/%d/%Y %H:%M')

    class Meta:
        model = BookReservation
        fields = ['id', 'book', 'user', 'reservation_date', 'expiration_date', 'is_active', 'is_confirmed', 'days']
        read_only_fields = ['user', 'is_active', 'is_confirmed']

    def create(self, validated_data):
        days = validated_data['days']
        expiration_date = datetime.now() + timedelta(days=days)
        reservation = BookReservation.objects.create(
            expiration_date=expiration_date,
            is_active=True,
            **validated_data
        )
        return reservation


class BookRentSerializer(serializers.ModelSerializer):
    total_rent_cost = serializers.SerializerMethodField()
    total_fine = serializers.SerializerMethodField()

    class Meta:
        model = BookRent
        fields = ['id', 'user', 'book', 'rent_date', 'return_date', 'daily_rate', 'fine_per_day', 'total_rent_cost',
                  'total_fine', 'status']

    def get_total_rent_cost(self, obj):
        return obj.calculate_total_rent_cost()

    def get_total_fine(self, obj):
        return obj.calculate_total_fine()


class RentSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    class Meta:
        fields = ('id',)
