from django.db import models
from car.models import Car
from user.models import Company, User


# Create your models here.

class Parking(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True)
    parking = models.ForeignKey(Parking, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    is_parking = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.car and self.parking:
            return f"{self.car}-{self.parking}"
        else:
            return f"start-{self.start}-end-{self.end}"


class Amount(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    val = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

