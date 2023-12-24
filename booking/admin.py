from django.contrib import admin
from .models import Booking, Parking, Amount

# Register your models here.
admin.site.register(Booking)
admin.site.register(Parking)
admin.site.register(Amount)
