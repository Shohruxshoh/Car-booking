from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from car.models import Car, CarType
from user.models import User


class UserCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class CarListSerializer(serializers.ModelSerializer):
    user = UserCarSerializer()

    class Meta:
        model = Car
        fields = ["user", "name", "color", "car_number", "car_type"]


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["user", "name", "color", "car_number", "car_type"]

    def validate(self, attrs):
        user = attrs.get("user")
        car_type = attrs.get("car_type")
        car_light = Car.objects.filter(user=user, car_type=CarType.LIGHT_CAR.value).count()
        truck = Car.objects.filter(user=user, car_type=CarType.TRUCK.value).count()
        if car_light > 2 and car_type == CarType.LIGHT_CAR.value:
            raise ValidationError({"success": False,
                                   "message": "Yelgil mashinalar soni 3tadan ko'p bo'lmasligi kerak. Sizda allaqachon 3ta mashina mavjud!"})
        elif truck > 1 and car_type == CarType.TRUCK.value:
            raise ValidationError({"success": False,
                                   "message": "Yuk mashinalar soni 2tadan ko'p bo'lmasligi kerak. Sizda allaqachon 2ta mashina mavjud!"})
        return attrs
