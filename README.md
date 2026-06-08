# Travel Agency (Django)

Full-stack travel booking application built with Django and PostgreSQL.

## Live demo

**Primary:**
https://pgolebiewski07.alwaysdata.net

**Backup:**
https://travel-agency-u5y1.onrender.com/

## Demo account
Use this account to test reviews.

> ⚠️ The backup Render deployment may take up to 1 minute to start after inactivity.

Login: demo  
Password: demo123

## Features

- Browse and search trips with advanced filtering
- Booking system with overbooking protection
- Dynamic price calculation (EUR / PLN)
- Trip reviews and rating system
- Multi-language support (PL / EN)
- User bookings panel
- Responsive Bootstrap UI
- Read-only REST API (Django REST Framework)
- PostgreSQL-backed production deployment
- Automated tests for booking and filtering logic

## Tech Stack

- Python, Django
- PostgreSQL (Neon)
- SQLite (local fallback for development)
- Bootstrap
- Django Templates
- Django REST Framework (read-only API for trips)

## Screenshots

![Home](screenshots/home.png)
![Trips](screenshots/trips.png)
![Details](screenshots/details.png)

## API

Example endpoints:
- GET /api/trips/
- GET /api/trips/{id}/

## Run Locally

```bash
git clone https://github.com/piotrgolebiewski07/travel_agency.git
cd travel_agency

python -m venv .venv
.venv\Scripts\activate  # Windows

pip install -r requirements.txt

# Create .env file and configure DATABASE_URL

python manage.py migrate
python seed_data.py
python manage.py runserver
```

## Seed data
The project includes `seed_data.py`, which populates the database with sample trips and reviews for local development and demo deployments.

---

## Deployment

### Production:
- Alwaysdata (Python WSGI hosting)
- Neon PostgreSQL

### Source code:
- GitHub

### Alternative Deployment:
- Render + Neon PostgreSQL
  
Environment variables:

```env
SECRET_KEY=your_secret_key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:password@host/database
```
---
## Tests
Basic test coverage for booking logic and filtering is included.
```bash
python manage.py test
```
  
## Architecture

GitHub → Alwaysdata (Django) → Neon PostgreSQL

## Key Concepts

- Django ORM with annotations (average rating, filtering)
- Overbooking protection logic
- Server-side rendering with Django templates
- REST API with Django REST Framework
- Production deployment using Alwaysdata, Render and Neon PostgreSQL
