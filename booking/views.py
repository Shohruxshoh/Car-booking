from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import pandas as pd
from django.http import HttpResponse
from car.models import BHM, Car, CarType
from carBooking.permissions import IsOwnerOrReadOnly, IsOwnerOrReadOnlyBooking, IsOwnerOrReadOnlyParking
from .models import Parking, Booking, Amount
from .serializers import ParkingSerializer, BookingSerializer, BookingListSerializer, AmountSerializer


# Create your views here.

# Parkovka yaratish va ro'xatini chiqarish uchun
class ParkingListCreateView(ListCreateAPIView):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    permission_classes = (IsAuthenticated,)


# Parkovka o'zgartirish va o'chirish uchun
class ParkingUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyParking,)


class ParkingGetOwnerView(ListAPIView):
    serializer_class = ParkingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        query = Parking.objects.filter(created_by=self.request.user)
        return query


class BookingCreateView(GenericAPIView):
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class BookingGiveUpView(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyBooking,)

    def post(self, request, pk, *args, **kwargs):
        booking = Booking.objects.filter(id=pk).first()
        booking.is_deleted = True
        booking.is_parking = False
        booking.save()
        return Response({"success": True, "message": "Bekor qilindi"})


class BookingListView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingListSerializer
    permission_classes = (IsAdminUser,)


class BookingUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyBooking,)


class BookingGetOwnerView(ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        query = Booking.objects.filter(car__user=self.request.user)
        return query


# To'lanadigan pullar hisobi
class AmountCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, *args, **kwargs):
        booking = Booking.objects.filter(id=pk).first()
        car = Car.objects.filter(id=booking.car.pk).first()
        company = booking.parking.company
        bhm = BHM.objects.first()
        sum = 0
        if car.car_type == CarType.LIGHT_CAR.value:
            sum = (bhm.bhm * bhm.car) / 100
        elif car.car_type == CarType.TRUCK.value:
            sum = (bhm.bhm * bhm.truck) / 100
        amount = Amount.objects.create(booking=booking, company=company, is_paid=True, val=sum)
        return Response({"success": True, "message": "To'landi!!!"})


class AmountListView(ListAPIView):
    queryset = Amount.objects.all()
    serializer_class = AmountSerializer
    permission_classes = (IsAdminUser,)


def booking_to_excel(request):
    # Model ma'lumotlarni olish
    queryset = Booking.objects.all()

    # QuerySet ni DataFrame ga o'zgartirish
    df = pd.DataFrame(list(queryset.values()))
    df['created_at'] = df['created_at'].apply(
        lambda x: x.replace(tzinfo=None) if x is not None else None)
    df['updated_at'] = df['updated_at'].apply(
        lambda x: x.replace(tzinfo=None) if x is not None else None)

    # Excel faylni yaratish
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="model_data.xlsx"'

    # DataFrame ni Excel faylga yozish
    df.to_excel(response, index=False, engine='openpyxl')

    return response


def amount_to_excel(request):
    # Model ma'lumotlarni olish
    queryset = Amount.objects.all()

    # QuerySet ni DataFrame ga o'zgartirish
    df = pd.DataFrame(list(queryset.values()))
    df['created_at'] = df['created_at'].apply(
        lambda x: x.replace(tzinfo=None) if x is not None else None)
    df['updated_at'] = df['updated_at'].apply(
        lambda x: x.replace(tzinfo=None) if x is not None else None)
    # Excel faylni yaratish
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="model_data.xlsx"'

    # DataFrame ni Excel faylga yozish
    df.to_excel(response, index=False, engine='openpyxl')

    return response
