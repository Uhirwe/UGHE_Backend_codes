# UGHE Test Web App — Backend (Django)

Django REST Framework backend for the University of Global Health Equity (UGHE) Test Web App.

## Stack

- Python 3.12
- Django 5.1
- Django REST Framework
- Simple JWT
- PostgreSQL
- Docker

## Quick start (Docker)

From the monorepo root (`UGHE-Test-Web-App/`):

```bash
docker compose up --build
```

Backend API: http://localhost:8000  
Django Admin: http://localhost:8000/admin/

## Local development (without full Compose)

```bash
cp .env.example .env
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Ensure PostgreSQL is running with credentials from .env
python manage.py migrate
python manage.py seed_data
python manage.py runserver 0.0.0.0:8000
```

## Test credentials

| Role | Username | Password |
|------|----------|----------|
| Admin (Django Admin + API) | `admin` | `UgheAdmin2024!` |
| Frontend test user | `ughe_user` | `UgheTest2024!` |

Credentials are configured via environment variables (see `.env.example`). Do not use these passwords in production.

## API endpoints

### Authentication

- `POST /api/auth/login/` — obtain JWT access + refresh tokens
- `POST /api/auth/refresh/` — refresh access token
- `POST /api/auth/logout/` — blacklist refresh token
- `GET /api/auth/me/` — current user

### Content (JWT required)

- `GET /api/content/navigation/`
- `GET /api/content/slides/`
- `GET /api/content/statistics/`
- `GET /api/content/sections/`
- `GET /api/content/settings/`
- `GET /api/health/` — health check (public)

## Managing content

1. Open http://localhost:8000/admin/
2. Log in with the admin credentials
3. Add/edit Navigation Items, Hero Slides, Statistics, Website Sections, and Site Settings
4. Upload images for slides via the admin form
5. Refresh the frontend to see updates

## Tests

```bash
python manage.py test
```

## Environment variables

See `.env.example` for the full list.

## License

Educational / assessment project. UGHE branding belongs to the University of Global Health Equity.
