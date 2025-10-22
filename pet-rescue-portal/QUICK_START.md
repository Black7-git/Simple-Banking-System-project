# PetRescue - Quick Start Guide

Get up and running with PetRescue in 5 minutes!

## Prerequisites
- Python 3.8+ installed
- Terminal/Command Prompt access

## Installation (5 steps)

### 1. Navigate to Project
```bash
cd /workspace/pet-rescue-portal
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Database (SQLite - easiest)
```bash
python manage.py migrate
```

### 4. Create Admin Account
```bash
python manage.py createsuperuser
```
Follow prompts to create username and password.

### 5. Start Server
```bash
python manage.py runserver
```

## Access the Application

Open your browser and visit:
- **Main Site**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## First Steps

1. **Login** with the superuser account you created
2. **Set Admin Privileges**:
   - Go to Django admin (http://127.0.0.1:8000/admin/)
   - Click "User profiles"
   - Find your profile
   - Check "Is admin" checkbox
   - Save
3. **Start Using**:
   - Report a pet at http://127.0.0.1:8000/pets/report/
   - Search pets at http://127.0.0.1:8000/pets/
   - Access admin panel at http://127.0.0.1:8000/admin-panel/

## Quick Troubleshooting

**Problem**: Can't install dependencies
```bash
# Try upgrading pip first
pip install --upgrade pip
pip install -r requirements.txt
```

**Problem**: Port 8000 already in use
```bash
python manage.py runserver 8080
```

**Problem**: MySQL errors
Edit `petrescue/settings.py` and use SQLite instead:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## Key Features

✅ Report lost/found pets
✅ Search pets with filters
✅ User authentication
✅ Admin management panel
✅ Request system
✅ Notifications
✅ Comments on pet reports

## Next Steps

- Read full [README.md](README.md) for detailed information
- Check [INSTALLATION.md](INSTALLATION.md) for advanced setup
- Review [TESTING.md](TESTING.md) for testing procedures

## Need Help?

- Check documentation files in project root
- Review Django documentation: https://docs.djangoproject.com/
- Contact: support@petrescue.com

---

**Note**: This quick start uses SQLite database. For production, configure MySQL. See INSTALLATION.md for details.
