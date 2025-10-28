# PetRescue - Pet Adoption and Rescue Management Portal

An interactive Django web platform to bridge the gap between people who find lost pets and their owners. Users can report found pets, search reports, and submit claims. Admins can review and manage reports and claims.

## Tech stack
- Django 5, Python 3.13
- SQLite (default) or MySQL via PyMySQL (configurable)
- Bootstrap 5, crispy-forms
- pytest for tests

## Features
- Report found pets with photo and contact details
- Search by species, color, location, and keywords
- Submit claims with optional proof image
- Email notifications to reporters on new claims and to claimers on status change
- Admin filters and actions to approve/reject claims and update report status
- User auth (signup/login/logout)

## Quick start

1. Create and activate virtualenv
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies
```bash
pip install -U pip setuptools wheel
pip install -r requirements.txt
```

3. Configure environment
```bash
cp .env.example .env
# Optionally set DB_ENGINE=mysql and fill MYSQL_* vars
```

4. Run migrations and start server
```bash
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000

## Running tests
```bash
pytest -q
```

## MySQL setup (optional)
Install server and client libs, then create database and user. Example on Ubuntu:
```bash
sudo apt-get install default-mysql-client default-libmysqlclient-dev
export DB_ENGINE=mysql MYSQL_DATABASE=petrescue MYSQL_USER=root MYSQL_PASSWORD=... MYSQL_HOST=127.0.0.1 MYSQL_PORT=3306
python manage.py migrate
```

## Project structure
- `config/` project settings and URLs
- `pets/` reports, claims, views, templates
- `accounts/` signup view and URLs
- `templates/` base and pages; `static/` assets; `media/` uploads

## Admin
```bash
python manage.py createsuperuser
```

## Notes
- Default email backend in `.env.example` is console for dev. Tests use locmem backend.
