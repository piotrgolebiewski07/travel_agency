from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TripViewSet
from . import views

router = DefaultRouter()
router.register(r"trips", TripViewSet,basename="trip")

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.trip_detail, name="detail"),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
]

