from rest_framework import serializers

from user.api.validators import check_phone_number
from user.models import User, RentalUser


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True, max_length=128, min_length=8)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'phone_number', 'first_name', 'last_name')

    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        if phone_number:
            if not check_phone_number(phone_number):
                raise serializers.ValidationError({'phone_number': "Telefon raqam noto'g'ri kiritildi"})
        user = User.objects.create_user(**validated_data)
        return user


class RentalUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = RentalUser
        fields = '__all__'
