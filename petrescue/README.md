# PetRescue - Pet Adoption and Rescue Management Portal

An interactive Django web platform to connect finders of lost pets with their owners.

## Features
- Report lost/found pets with photos and details
- Search and view reports by code, location, species, and more
- Admin management via Django admin
- Email notifications on report creation and status changes

## Tech Stack
- Django 5, Python 3.13
- SQLite by default; MySQL via environment variables
- Templates + basic CSS for UI

## Quick Start
```bash
# 1) Create virtualenv and install deps
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 2) Env vars
cp .env.example .env
# Edit .env for MySQL if desired (else SQLite is used)

# 3) Run migrations and dev server
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## MySQL Config (optional)
Set these in `.env` to use MySQL instead of SQLite:
- `DB_ENGINE=django.db.backends.mysql`
- `DB_NAME=petrescue`
- `DB_USER=petrescue`
- `DB_PASSWORD=...`
- `DB_HOST=127.0.0.1`
- `DB_PORT=3306`

## Running Tests
```bash
python manage.py test
```
