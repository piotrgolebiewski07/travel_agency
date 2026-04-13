# 1. Standard library

# 2. Django
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django_filters.rest_framework import DjangoFilterBackend

# 3. Third-party (DRF)
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter

# 4. Local imports
from .models import Trip, ContactMessage
from .serializers import TripSerializer
from .forms import ReviewForm, ContactForm


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
        queryset = Trip.objects.annotate(
            avg_rating=Avg("reviews__rating"),
            reviews_count=Count("reviews")
        ).order_by("start_date")

        min_rating = self.request.query_params.get("min_rating")

        if min_rating:
            queryset = queryset.filter(avg_rating__gte=float(min_rating))

        return queryset


def home(request):
    trips = Trip.objects.all().annotate(
        avg_rating=Avg("reviews__rating"),
        reviews_count=Count("reviews")
    ).order_by("start_date")[:3]

    return render(request, "home.html", {"trips": trips})


def index(request):
    trips = Trip.objects.prefetch_related("images", "reviews").annotate(
        avg_rating=Avg("reviews__rating"),
        reviews_count=Count("reviews")
    ).order_by("start_date")

    locations = Trip.objects.values_list("location", flat=True).distinct().order_by("location")
    countries = Trip.objects.values_list("country", flat=True).distinct().order_by("country")

    country = request.GET.get("country")
    location = request.GET.get("location")
    min_price = safe_float(request.GET.get("min_price"))
    max_price = safe_float(request.GET.get("max_price"))
    min_rating = safe_float (request.GET.get("min_rating"))
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    available = request.GET.get("available")
    search = request.GET.get("search")
    sort = request.GET.get("sort")

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

    paginator = Paginator(trips, 5)  # 5 trips na stronę
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "trips/index.html", {
        "trips": page_obj,
        "locations": locations,
        "countries": countries
    })


def trip_detail(request, pk):
    trip = get_object_or_404(
        Trip.objects.prefetch_related("images", "reviews"),
        pk=pk
    )

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")

        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.trip = trip
            review.save()
            return redirect("detail", pk=pk)
    else:
        form = ReviewForm()

    return render(request, "trips/detail.html", {
        "trip": trip,
        "form": form
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