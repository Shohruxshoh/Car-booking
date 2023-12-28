from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from datetime import timedelta, date, datetime
from booking.models import Parking, Booking, Amount
from car.serializers import CarListSerializer
from user.models import Company
from user.serializers import UserGetSerializer


# kompaniya CRUD
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["user", "name", "phone", "address"]


# Parkovka serializer CRUD uchun
class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = ['company', 'name', 'created_by']


class ParkingListSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    created_by = UserGetSerializer()

    class Meta:
        model = Parking
        fields = ['company', 'name', 'created_by']


#   Band qilish uchun serializer
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['car', 'parking', 'date', 'start', 'end']

    def validate(self, attrs):
        car = attrs.get('car')
        parking = attrs.get('parking')
        date1 = attrs.get('date')
        start = attrs.get('start')
        end = attrs.get('end')
        booking_day = Booking.objects.filter(car=car, parking=parking, date=date1)
        booking = Booking.objects.filter(car=car, is_parking=True)
        booked_slot = Booking.objects.filter(parking=parking, date=date1, start__range=[start, end],
                                             end__range=[start, end], is_parking=True)

        if booking.exists():
            raise ValidationError({"success": False, "message": "Bu mashina parkovka qilingan!"})

        if booked_slot.exists():
            raise ValidationError({"success": False, "message": "Bu joy band siz qo'ymoqchi bo'lgan vaqtda!"})

        print(self.is_booking_day_valid(booking_day, start, end))

        if booking_day and self.is_booking_day_valid(booking_day, start, end):
            raise ValidationError({"success": False, "message": "Bir kunda 3 soatdan ko'p foydalanish mumkin emas!"})

        return attrs

    @staticmethod
    def is_booking_day_valid(booking_day, start, end):
        start_datetime = datetime.combine(date.today(), start)
        end_datetime = datetime.combine(date.today(), end)
        time_difference1 = timedelta(hours=0)
        for booking in booking_day:
            start_datetime1 = datetime.combine(date.today(), booking.start)
            end_datetime1 = datetime.combine(date.today(), booking.end)
            time_difference1 += end_datetime1 - start_datetime1
            print(time_difference1)

        time_difference = end_datetime - start_datetime
        time_difference2 = time_difference1 + time_difference
        return time_difference2 >= timedelta(hours=3)


class BookingListSerializer(serializers.ModelSerializer):
    car = CarListSerializer()
    parking = ParkingSerializer()

    class Meta:
        model = Booking
        fields = ['car', 'parking', 'date', 'start', 'end', "is_parking", 'is_deleted', 'created_at', 'updated_at']


class AmountSerializer(serializers.ModelSerializer):
    booking = BookingListSerializer(read_only=True)
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Amount
        fields = ["booking", "company", "val", "is_paid", "created_at", "updated_at"]
