from django.db import models
from decimal import Decimal
from django.utils import translation
from django.contrib.auth.models import User


class Trip(models.Model):
    title_pl = models.CharField(max_length=100)
    title_en = models.CharField(max_length=100)
    description_pl = models.TextField(max_length=1000)
    description_en = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=3, default="EUR")
    start_date = models.DateField()
    end_date = models.DateField()
    country = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    max_people = models.IntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title_pl or self.title_en

    def get_price_display(self):
        lang = translation.get_language()

        if lang == "pl":
            if self.currency == "EUR":
                return f"{int(self.price * Decimal('4.26'))} zł"
            return f"{int(self.price)} zł"

        return f"{int(self.price)} €"

    def calculate_total_price(self, adults, children):
        adults = int(adults or 0)
        children = int(children or 0)

        total = (adults * self.price + children * self.price * Decimal("0.8"))

        return int(total)

    def get_total_price_display(self, adults, children):
        total = self.calculate_total_price(adults, children)
        lang = translation.get_language()

        if lang == "pl":
            if self.currency == "EUR":
                return f"{int(total * Decimal('4.26'))} zł"
            return f"{int(total)} zł"

        return f"{int(total)} €"


class TripImage(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="images")  # delete images when Trip is deleted
    image = models.ImageField(upload_to="trips/")
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.trip.title_pl or self.trip.title_en }"


class Review(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="reviews")
    name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.trip.title_pl or self.trip.title_en}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


class Booking(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="bookings")
    adults = models.IntegerField()
    children = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="bookings")

    def __str__(self):
        return f"{self.trip} - {self.total_people} people ({self.created_at.date()})"

    @property
    def total_people(self):
        return self.adults + self.children

