# 1. Standard library

# 2. Django
from django.shortcuts import render, get_object_or_404

# 3. Third-party (DRF)
from rest_framework.viewsets import ModelViewSet

# 4. Local imports
from .models import Trip
from .serializers import TripSerializer


class TripViewSet(ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer


def trip_detail(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    return render(request, "trips/detail.html", {"trip": trip})


def home(request):
    trips = Trip.objects.all().order_by("start_date")[:3]
    return render(request, "home.html", {"trips": trips})


def index(request):
    trips = Trip.objects.all().order_by("start_date")  # pobiera dane

    location = request.GET.get("location")

    if location:
        trips = trips.filter(location__icontains=location)

    locations = Trip.objects.values_list("location", flat=True).distinct()

    return render(request, "trips/index.html", {
        "trips": trips,
        "locations": locations
    })

