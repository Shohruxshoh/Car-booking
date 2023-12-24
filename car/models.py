from enum import Enum

from django.db import models

from user.models import User


# Create your models here.

class CarType(Enum):
    TRUCK = "Truck"
    LIGHT_CAR = "Light car"


class Car(models.Model):
    TYPE_CHOICE = (
        (CarType.TRUCK.value, "Yuk mashina"),
        (CarType.LIGHT_CAR.value, "Yelgil mashina"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    car_number = models.CharField(max_length=200, unique=True)
    car_type = models.CharField(max_length=20, choices=TYPE_CHOICE, default=CarType.LIGHT_CAR.value)

    def __str__(self):
        return f"{self.user.username}-{self.name}-{self.car_number}"


class BHM(models.Model):
    bhm = models.IntegerField(default=0)
    car = models.IntegerField(default=0)
    truck = models.IntegerField(default=0)

    def __str__(self):
        return str(self.bhm)
