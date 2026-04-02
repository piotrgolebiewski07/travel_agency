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

    locations = Trip.objects.values_list("location", flat=True).distinct().order_by("location")
    countries = Trip.objects.values_list("country", flat=True).distinct().order_by("country")

    country = request.GET.get("country")
    location = request.GET.get("location")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    available = request.GET.get("available")

    if country:
        trips = trips.filter(country=country)

    if location:
        trips = trips.filter(location__icontains=location)

    if min_price:
        trips = trips.filter(price__gte=min_price)

    if max_price:
        trips = trips.filter(price__lte=max_price)

    if start_date:
        trips = trips.filter(start_date__gte=start_date)

    if end_date:
        trips = trips.filter(end_date__lte=end_date)

    if available:
        trips = trips.filter(available=True)

    return render(request, "trips/index.html", {
        "trips": trips,
        "locations": locations,
        "countries": countries
    })

