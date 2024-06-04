from rest_framework import serializers
from ..models import Book, StarsBook, StarsOfUsers


class StarsBookSerializer(serializers.ModelSerializer):
    average_rating = serializers.ReadOnlyField()

    class Meta:
        model = StarsBook
        fields = ['star', 'sum_rate', 'number_of_raters', 'average_rating']


class StarsOfUsersSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Assuming User model's __str__ method returns the username

    class Meta:
        model = StarsOfUsers
        fields = ['user', 'star', 'description']


class BookSerializer(serializers.ModelSerializer):
    star = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    comments = StarsOfUsersSerializer(source='stars', many=True)

    class Meta:
        model = Book
        fields = '__all__'

    def get_star(self, obj):
        stars_book = StarsBook.objects.filter(book=obj).first()
        return stars_book.star if stars_book else 0

    def get_average_rating(self, obj):
        stars_book = StarsBook.objects.filter(book=obj).first()
        return stars_book.average_rating if stars_book else 0


class RateBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = StarsOfUsers
        fields = ['book', 'user', 'star', 'description']

    def create(self, validated_data):
        book = validated_data.get('book')
        user = validated_data.get('user')
        star = validated_data.get('star')

        # Update StarsBook table
        stars_book, created = StarsBook.objects.get_or_create(book=book)
        stars_book.sum_rate += star
        stars_book.number_of_raters += 1
        stars_book.star = stars_book.sum_rate // stars_book.number_of_raters
        stars_book.save()

        stars_of_user, created = StarsOfUsers.objects.update_or_create(
            book=book,
            user=user,
            defaults={'star': star, 'description': validated_data.get('description')}
        )

        return stars_of_user
