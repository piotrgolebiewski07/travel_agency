from django.test import TestCase
from django.contrib.auth.models import User
from .models import Trip, Booking
from django.urls import reverse
from datetime import date


class BookingTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test", password="1234")

        self.trip = Trip.objects.create(
            title_pl="Test",
            title_en="Test",
            description_pl="Opis",
            description_en="Desc",
            price=100,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 5),
            country="PL",
            location="Warsaw",
            max_people=5,
            available=True
        )

    def test_booking_success(self):
        self.client.login(username="test", password="1234")

        response = self.client.post(
            reverse("detail", args=[self.trip.id]),
            {
                "booking": "1",
                "adults": 2,
                "children": 1
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Booking.objects.count(), 1)

    def test_overbooking_blocked(self):
        self.client.login(username="test", password="1234")

        Booking.objects.create(
            trip=self.trip,
            adults=4,
            children=0,
            total_price=400
        )

        response = self.client.post(
            reverse("detail", args=[self.trip.id]),
            {
                "booking": "1",
                "adults": 3,
                "children": 0
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertContains(response, "Too many people selected")

    def test_booking_exact_limit_allowed(self):
        self.client.login(username="test", password="1234")

        Booking.objects.create(
            trip=self.trip,
            adults=3,
            children=0,
            total_price=300
        )

        response = self.client.post(
            reverse("detail", args=[self.trip.id]),
            {
                "booking": "1",
                "adults": 2,
                "children": 0
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Booking.objects.count(), 2)

    def test_booking_without_login_allowed(self):
        response = self.client.post(
            reverse("detail", args=[self.trip.id]),
            {
                "booking": "1",
                "adults": 2,
                "children": 0
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Booking.objects.count(), 1)

    def test_no_available_places(self):
        self.client.login(username="test", password="1234")

        Booking.objects.create(
            trip=self.trip,
            adults=5,
            children=0,
            total_price=500
        )

        response = self.client.get(
            reverse("detail", args=[self.trip.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Available places")

