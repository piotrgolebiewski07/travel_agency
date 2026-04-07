from django.db import models


class Trip(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=3, default="EUR")
    start_date = models.DateField()
    end_date = models.DateField()
    country = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    max_people = models.IntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_currency_symbol(self):
        if self.currency == "EUR":
            return "€"
        if self.currency == "PLN":
            return "zł"


class TripImage(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="images")  # delete images when Trip is deleted
    image = models.ImageField(upload_to="trips/")
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.trip.title}"


class Review(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="reviews")
    name = models.CharField(max_length=100)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.trip.title}"

