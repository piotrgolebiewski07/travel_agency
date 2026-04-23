# 1. Standard library
from datetime import timedelta
import requests
from decimal import Decimal

# 2. Django
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q, F, ExpressionWrapper, DurationField
from django_filters.rest_framework import DjangoFilterBackend
from django.db import connection
from django.conf import settings
from django.contrib.auth.decorators import login_required

# 3. Third-party (DRF)
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter

# 4. Local imports
from .models import Trip, ContactMessage, Booking
from .serializers import TripSerializer
from .forms import ReviewForm, ContactForm


def normalize_guests(request):
    adults = int(request.GET.get("adults") or 1)
    children = int(request.GET.get("children") or 0)

    if adults < 1:
        adults = 1

    if children < 0:
        children = 0

    if adults > 8:
        adults = 8
        children = 0
    elif adults + children > 8:
        children = 8 - adults

    total_people = adults + children
    return adults, children, total_people


def get_filtered_trips(request):
    trips = Trip.objects.prefetch_related("images", "reviews").annotate(
        avg_rating=Avg("reviews__rating"),
        reviews_count=Count("reviews"),
        duration=ExpressionWrapper(
            F("end_date") - F("start_date") + timedelta(days=1),
            output_field=DurationField()
        )
    )

    country = request.GET.get("country")
    location = request.GET.get("location")
    min_price = safe_float(request.GET.get("min_price"))
    max_price = safe_float(request.GET.get("max_price"))
    min_rating = safe_float(request.GET.get("min_rating"))
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    available = request.GET.get("available")
    search = request.GET.get("search")
    sort = request.GET.get("sort")

    adults, children, total_people = normalize_guests(request)

    min_days = safe_float(request.GET.get("min_days"))
    max_days = safe_float(request.GET.get("max_days"))

    if country:
        trips = trips.filter(country=country)

    if location:
        trips = trips.filter(location__icontains=location)

    if min_price is not None:
        trips = trips.filter(price__gte=min_price)

    if max_price is not None:
        trips = trips.filter(price__lte=max_price)

    if start_date:
        trips = trips.filter(start_date__gte=start_date)

    if end_date:
        trips = trips.filter(end_date__lte=end_date)

    if available:
        trips = trips.filter(available=True)

    if min_rating is not None:
        trips = trips.filter(avg_rating__gte=min_rating)

    if search:
        trips = trips.filter(
            Q(title_pl__icontains=search) |
            Q(title_en__icontains=search) |
            Q(country__icontains=search) |
            Q(location__icontains=search) |
            Q(description_pl__icontains=search) |
            Q(description_en__icontains=search)
        ).distinct().order_by("-start_date")

    if sort == "price_asc":
        trips = trips.order_by("price")
    elif sort == "price_desc":
        trips = trips.order_by("-price")
    elif sort == "rating":
        trips = trips.order_by("-avg_rating")
    elif sort == "start_date":
        trips = trips.order_by("start_date")
    elif sort == "end_date":
        trips = trips.order_by("-end_date")

    if total_people > 0:
        trips = trips.filter(max_people__gte=total_people)

    if min_days is not None:
        trips = trips.filter(duration__gte=timedelta(days=min_days))

    if max_days is not None:
        trips = trips.filter(duration__lte=timedelta(days=max_days))

    return trips


class TripViewSet(ModelViewSet):
    serializer_class = TripSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = {
        "price": ["gte", "lte"],
        "country": ["exact"],
        "start_date": ["gte", "lte"],
        "available": ["exact"],
    }
    ordering_fields = ["price", "avg_rating", "reviews_count", "start_date"]
    search_fields = ["title_pl", "title_en", "country", "location", "description_pl", "description_en"]

    def get_queryset(self):
        return get_filtered_trips(self.request)


def home(request):
    trips = Trip.objects.all().annotate(
        avg_rating=Avg("reviews__rating"),
        reviews_count=Count("reviews"),
        duration=ExpressionWrapper(
            F("end_date") - F("start_date") + timedelta(days=1),
            output_field=DurationField()
        )
    ).order_by("start_date")[:3]

    rate = get_eur_to_pln_rate()

    for trip in trips:
        trip.price_pln = trip.price * Decimal(str(rate))
        trip.duration_days = trip.duration.days

    return render(request, "home.html", {"trips": trips})


def index(request):
    trips = get_filtered_trips(request)

    locations = Trip.objects.values_list("location", flat=True).distinct().order_by("location")
    countries = Trip.objects.values_list("country", flat=True).distinct().order_by("country")

    paginator = Paginator(trips, 5)  # 5 trips na stronę
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    adults, children, total_people = normalize_guests(request)
    rate = get_eur_to_pln_rate()

    price_type = request.GET.get("price_type", "person")

    raw_adults = int(request.GET.get("adults") or 1)
    raw_children = int(request.GET.get("children") or 0)

    limit_exceeded = (raw_adults + raw_children) > 8

    for trip in page_obj:
        trip.total_price_eur = trip.calculate_total_price(adults, children)
        trip.total_price_pln = trip.total_price_eur * Decimal(str(rate))
        trip.price_pln = trip.price * Decimal(str(rate))
        trip.duration_days = trip.duration.days

    if settings.DEBUG:
        print("SQL queries:", len(connection.queries))

    return render(request, "trips/index.html", {
        "trips": page_obj,
        "locations": locations,
        "countries": countries,
        "total_people": total_people,
        "price_type": price_type,
        "adults": adults,
        "children": children,
        "limit_exceeded": limit_exceeded,
    })


def trip_detail(request, pk):
    trip = get_object_or_404(
        Trip.objects.prefetch_related("images", "reviews"),
        pk=pk
    )

    adults = int(request.GET.get("adults") or 1)
    children = int(request.GET.get("children") or 0)

    raw_adults = int(request.GET.get("adults") or 1)
    raw_children = int(request.GET.get("children") or 0)

    if adults < 1:
        adults = 1

    if children < 0:
        children = 0

    max_allowed = min(trip.max_people, 8)

    if adults > max_allowed:
        adults = max_allowed
        children = 0

    elif adults + children > max_allowed:
        children = max_allowed - adults

    rate = get_eur_to_pln_rate()

    total_price_eur = trip.calculate_total_price(adults, children)
    total_price_pln = total_price_eur * Decimal(str(rate))

    if request.method == "POST":

        # BOOKING
        if "booking" in request.POST:
            adults = int(request.POST.get("adults") or 1)
            children = int(request.POST.get("children") or 0)

            if adults < 1:
                adults = 1

            if children < 0:
                children = 0
            booked_people = sum(b.adults + b.children for b in trip.bookings.all())
            new_people = adults + children

            if booked_people + new_people > trip.max_people:
                form = ReviewForm()
                return render(request, "trips/detail.html", {
                    "trip": trip,
                    "form": form,
                    "total_price_eur": total_price_eur,
                    "total_price_pln": total_price_pln,
                    "adults": adults,
                    "children": children,
                    "max_allowed": max_allowed,
                    "limit_exceeded": True,
                    "no_availability": True,  # 🔥 komunikat
                })

            raw_total = trip.calculate_total_price(adults, children)

            Booking.objects.create(
                trip=trip,
                user=request.user if request.user.is_authenticated else None,
                adults=adults,
                children=children,
                total_price=raw_total
            )

            total_price_eur = trip.calculate_total_price(adults, children)
            total_price_pln = total_price_eur * Decimal(str(rate))

            return render(request, "trips/booking_confirmation.html", {
                "trip": trip,
                "adults": adults,
                "children": children,
                "total_price_eur": total_price_eur,
                "total_price_pln": total_price_pln,
            })

        # REVIEW
        if not request.user.is_authenticated:
            return redirect("login")

        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.trip = trip
            review.save()
            return redirect("detail", pk=pk)

    form = ReviewForm()

    limit_exceeded = (raw_adults + raw_children) > max_allowed

    return render(request, "trips/detail.html", {
        "trip": trip,
        "form": form,
        "total_price_eur": total_price_eur,
        "total_price_pln": total_price_pln,
        "adults": adults,
        "children": children,
        "max_allowed": max_allowed,
        "limit_exceeded": limit_exceeded,
    })


def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data["your_name"],
                email=form.cleaned_data["your_email"],
                message=form.cleaned_data["your_message"],
            )

            return redirect("thanks")

    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})


def thanks(request):
    return render(request, "thanks.html")


@login_required
def my_bookings(request):
    bookings = request.user.bookings.all().order_by("-created_at")

    rate = get_eur_to_pln_rate()

    for booking in bookings:
        booking.price_pln = booking.total_price * Decimal(str(rate))

    return render(request, "trips/my_bookings.html", {
        "bookings": bookings,
    })


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        booking.delete()

    return redirect("my_bookings")


def get_eur_to_pln_rate():
    try:
        response = requests.get("https://open.er-api.com/v6/latest/EUR")
        data = response.json()
        return data["rates"]["PLN"]
    except Exception as e:
        print("ERROR:", e)
        return 4.22

