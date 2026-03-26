# 1. Standard library

# 2. Django
from django.shortcuts import render, get_object_or_404

# 3. Third-party (DRF)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

# 4. Local imports
from .models import Trip
from .serializers import TripSerializer


def trip_detail(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    return render(request, "trips/detail.html", {"trip": trip})


def home(request):
    trips = Trip.objects.all().order_by("start_date")[:3]
    return render(request, "home.html", {"trips": trips})


def index(request):
    trips = Trip.objects.all().order_by("start_date")  # pobiera dane
    return render(request, "trips/index.html", {"trips": trips})  # przekazuje dane do template


@api_view(["GET", "POST"])
def api_trips(request):
    if request.method == "GET":
        trips = Trip.objects.all()
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = TripSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def api_trip_detail(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    serializer = TripSerializer(trip)
    return Response(serializer.data)

