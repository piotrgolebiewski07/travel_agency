from django.db import models


class Trip(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=3, default="EUR")
    start_date = models.DateField()
    end_date = models.DateField()
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

