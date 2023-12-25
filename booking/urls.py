from django.urls import path

from booking.views import ParkingListView, ParkingUpdateDeleteView, BookingCreateView, BookingUpdateDeleteView, \
    BookingListView, BookingGiveUpView, AmountCreateView, booking_to_excel, amount_to_excel, AmountListView, \
    ParkingGetOwnerView, BookingGetOwnerView, ParkingCreateView

urlpatterns = [
    # Parkovka yaratish
    path('parking/', ParkingListView.as_view()),
    path('parking-create/', ParkingCreateView.as_view()),
    path('parking/owner/', ParkingGetOwnerView.as_view()),
    path('parking/<int:pk>/', ParkingUpdateDeleteView.as_view()),
    # Booking
    path('', BookingListView.as_view()),
    path('owner/', BookingGetOwnerView.as_view()),
    path('create/', BookingCreateView.as_view()),
    path('<int:pk>/', BookingUpdateDeleteView.as_view()),
    path('give-up/<int:pk>/', BookingGiveUpView.as_view()),

    # To'lov
    path("amount/", AmountListView.as_view()),
    path('pay/<int:pk>/', AmountCreateView.as_view()),

    # excel
    path("booking-excel/", booking_to_excel, name='booking-excel'),
    path("amount-excel/", amount_to_excel, name="amount-excel"),
]
