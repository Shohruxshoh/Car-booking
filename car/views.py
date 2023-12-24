from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from car.models import Car
from car.serializers import CarSerializer, CarListSerializer
from carBooking.permissions import IsOwnerOrReadOnly


# Create your views here.

class CarApiCreateView(CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (IsAuthenticated,)


class CarApiListView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarListSerializer
    permission_classes = (IsAuthenticated,)


class CarApiUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)


class CarGetOwnerView(ListAPIView):
    serializer_class = CarSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        query = Car.objects.filter(user=self.request.user)
        return query
