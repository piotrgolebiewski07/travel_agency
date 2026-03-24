from django.shortcuts import render, get_object_or_404
from .models import Trip


def trip_detail(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    return render(request, "trips/detail.html", {"trip": trip})


def home(request):
    trips = Trip.objects.all().order_by("start_date")[:3]
    return render(request, "home.html", {"trips": trips})


def index(request):
    trips = Trip.objects.all().order_by("start_date")  # pobiera dane
    return render(request, "trips/index.html", {"trips": trips})  # przekazuje dane do template

