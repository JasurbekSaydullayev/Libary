from rest_framework import serializers

from books.models import Book


class BookSerializer(serializers.ModelSerializer):
    number_of_raters = serializers.IntegerField(read_only=True)
    star = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'
