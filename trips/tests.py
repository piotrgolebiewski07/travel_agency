# 1. Standard library
from datetime import date

# 2. Django
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse

# 3. Local imports
from .models import Trip, Booking
from .views import get_filtered_trips, normalize_guests


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


class FilterTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()  # create false request

        # Trip 1
        self.trip1 = Trip.objects.create(
            title_pl="Hiszpania",
            title_en="Spain",
            description_pl="Opis",
            description_en="Desc",
            price=100,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 5),
            country="Spain",
            location="Barcelona",
            max_people=5,
            available=True
        )

        # Trip 2
        self.trip2 = Trip.objects.create(
            title_pl="Włochy",
            title_en="Italy",
            description_pl="Opis",
            description_en="Desc",
            price=200,
            start_date=date(2026, 2, 1),
            end_date=date(2026, 2, 5),
            country="Italy",
            location="Rome",
            max_people=5,
            available=True
        )

    def test_filter_by_country(self):
        request = self.factory.get("/trips/?country=Spain")
        trips = get_filtered_trips(request)

        self.assertEqual(trips.count(), 1)
        self.assertEqual(trips.first(), self.trip1)

    def test_filter_by_min_price(self):
        request = self.factory.get("/trips/?min_price=150")
        trips = get_filtered_trips(request)

        self.assertEqual(trips.count(), 1)
        self.assertEqual(trips.first(), self.trip2)

    def test_search(self):
        request = self.factory.get("/trips/?search=Spain")
        trips = get_filtered_trips(request)

        self.assertEqual(trips.count(), 1)
        self.assertEqual(trips.first(), self.trip1)

    def test_sort_price_asc(self):
        request = self.factory.get("/trips/?sort=price_asc")
        trips = list(get_filtered_trips(request))

        self.assertEqual(trips[0], self.trip1)
        self.assertEqual(trips[1], self.trip2)

    def test_sort_price_desc(self):
        request = self.factory.get("/trips/?sort=price_desc")
        trips = list(get_filtered_trips(request))

        self.assertEqual(trips[0], self.trip2)
        self.assertEqual(trips[1], self.trip1)


class NormalizeTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_default_values(self):
        request = self.factory.get("/trips/")
        adults, children, total = normalize_guests(request)

        self.assertEqual(adults, 1)
        self.assertEqual(children, 0)
        self.assertEqual(total, 1)

    def test_negative_values(self):
        request = self.factory.get("/trips/?adults=-5&children=-3")
        adults, children, total = normalize_guests(request)

        self.assertEqual(adults, 1)
        self.assertEqual(children, 0)

    def test_max_people_limit(self):
        request = self.factory.get("/trips/?adults=6&children=5")
        adults, children, total = normalize_guests(request)

        self.assertEqual(total, 8)

    def test_adults_over_limit(self):
        request = self.factory.get("/trips/?adults=10&children=2")
        adults, children, total = normalize_guests(request)

        self.assertEqual(adults, 8)
        self.assertEqual(children, 0)

    def test_normal_values(self):
        request = self.factory.get("/trips/?adults=3&children=2")
        adults, children, total = normalize_guests(request)

        self.assertEqual(adults, 3)
        self.assertEqual(children, 2)
        self.assertEqual(total, 5)