from django.shortcuts import render
from .models import Trip


def index(request):
    trips = Trip.objects.all().order_by("start_date")  # pobiera dane

    return render(request, "trips/index.html", {"trips": trips})  # przekazuje dane do template



