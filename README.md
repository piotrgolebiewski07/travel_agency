# Travel Agency (Django)

Web application for browsing and booking trips with availability control and filtering.

## Features

- Browse trips with images and descriptions
- Booking system with overbooking protection
- Dynamic price calculation (EUR / PLN)
- Available places tracking
- Advanced filtering (country, price, rating, duration)
- Search and sorting
- Multi-language (PL / EN)
- User bookings panel
- Test coverage for booking logic, availability, and filtering

## Tech Stack

- Python, Django
- SQLite
- Bootstrap
- Django Templates
- Django REST Framework (basic API)

## Run locally
```bash
git clone https://github.com/piotrgolebiewski07/travel_agency.git
cd travel_agency

python -m venv .venv
.venv\Scripts\activate  # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
## Open in browser

http://127.0.0.1:8000/

## Tests
```bash
python manage.py test
```
## Demo

Coming soon.
