from django.urls import path
from .views import CarApiCreateView, CarApiUpdateView, CarApiListView, CarGetOwnerView

urlpatterns = [
    path("create/", CarApiCreateView.as_view(), name='car-create'),
    path("list/", CarApiListView.as_view(), name='cars'),
    path("owner/", CarGetOwnerView.as_view(), name='owner'),
    path("<int:pk>/", CarApiUpdateView.as_view(), name='car-update'),
]
