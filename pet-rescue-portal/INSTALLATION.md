# PetRescue Installation Guide

This guide provides detailed instructions for installing and setting up the PetRescue Pet Adoption and Rescue Management Portal.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Quick Start](#quick-start)
3. [Detailed Installation](#detailed-installation)
4. [Database Configuration](#database-configuration)
5. [Creating Admin User](#creating-admin-user)
6. [Running the Application](#running-the-application)
7. [Testing the Setup](#testing-the-setup)

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Disk Space**: 500MB free space
- **Database**: MySQL 8.0+ or SQLite3

### Software Dependencies
- Python 3.8+
- pip (Python package manager)
- MySQL Server (optional, for production)
- Git (for version control)

## Quick Start

For experienced users who want to get started quickly:

```bash
# Navigate to project directory
cd /workspace/pet-rescue-portal

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to access the application.

## Detailed Installation

### Step 1: Verify Python Installation

Check if Python is installed:
```bash
python --version
# or
python3 --version
```

You should see Python 3.8 or higher. If not, download from [python.org](https://www.python.org/downloads/).

### Step 2: Navigate to Project Directory

```bash
cd /workspace/pet-rescue-portal
```

### Step 3: Create Virtual Environment (Recommended)

Creating a virtual environment isolates project dependencies:

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Django 4.2.7
- mysqlclient 2.2.0
- Pillow 10.1.0
- python-decouple 3.8

### Step 5: Configure Database

#### Option A: SQLite (Recommended for Development)

SQLite requires no additional setup. Edit `petrescue/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### Option B: MySQL (Recommended for Production)

1. **Install MySQL Server**
   - Download from [MySQL Downloads](https://dev.mysql.com/downloads/)
   - Follow installation instructions for your OS

2. **Create Database**
   ```sql
   mysql -u root -p
   CREATE DATABASE petrescue_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'petrescue_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON petrescue_db.* TO 'petrescue_user'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

3. **Update Django Settings**
   
   Edit `petrescue/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'petrescue_db',
           'USER': 'petrescue_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '3306',
           'OPTIONS': {
               'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
           }
       }
   }
   ```

### Step 6: Run Database Migrations

Create database tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

Expected output:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, pets, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

### Step 7: Create Static and Media Directories

```bash
# Create media directory for uploaded photos
mkdir -p media/pet_photos

# Create static files directory
mkdir -p staticfiles
```

### Step 8: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

## Creating Admin User

Create a superuser account for admin access:

```bash
python manage.py createsuperuser
```

You'll be prompted to enter:
- Username
- Email address
- Password (enter twice)

Example:
```
Username: admin
Email address: admin@petrescue.com
Password: ********
Password (again): ********
Superuser created successfully.
```

### Set Admin Privileges

After creating the superuser, you need to mark them as admin in the system:

1. Start the server (see next section)
2. Login with superuser credentials
3. Access Django admin at http://127.0.0.1:8000/admin/
4. Go to "User profiles"
5. Find your user profile
6. Check the "Is admin" checkbox
7. Save

Alternatively, use Django shell:
```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from pets.models import UserProfile

user = User.objects.get(username='admin')
profile, created = UserProfile.objects.get_or_create(user=user)
profile.is_admin = True
profile.save()
exit()
```

## Running the Application

### Development Server

Start the Django development server:

```bash
python manage.py runserver
```

Expected output:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
October 22, 2025 - 10:00:00
Django version 4.2.7, using settings 'petrescue.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Access the application:
- **Main Site**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **User Admin**: http://127.0.0.1:8000/admin-panel/

### Running on Different Port

```bash
python manage.py runserver 8080
```

### Running on Different Host

```bash
python manage.py runserver 0.0.0.0:8000
```

## Testing the Setup

### 1. Access Home Page

Open http://127.0.0.1:8000/ in your browser. You should see:
- Navigation menu
- Hero section
- Statistics (will be 0 initially)
- How It Works section

### 2. Test User Registration

1. Click "Register" in navigation
2. Fill out the registration form
3. Submit and verify you're logged in

### 3. Test Pet Reporting

1. Login with your account
2. Click "Report Pet"
3. Fill out the form with test data
4. Upload a test image (optional)
5. Submit and verify the pet appears

### 4. Test Admin Access

1. Login with superuser account
2. Verify "Admin Panel" appears in navigation
3. Access admin panel
4. Verify you can see statistics

### 5. Test Search Functionality

1. Go to "Find Pets"
2. Try different search filters
3. Verify search results display correctly

## Troubleshooting

### Issue: `mysqlclient` Installation Error

**Windows:**
```bash
pip install wheel
pip install mysqlclient
```

If still failing, download the wheel file from [PyPI](https://pypi.org/project/mysqlclient/#files) and install:
```bash
pip install mysqlclient-2.2.0-cp310-cp310-win_amd64.whl
```

**Linux:**
```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
pip install mysqlclient
```

**macOS:**
```bash
brew install mysql-client
export PATH="/usr/local/opt/mysql-client/bin:$PATH"
pip install mysqlclient
```

### Issue: Pillow Installation Error

**Windows:**
Download and install from [Pillow website](https://pillow.readthedocs.io/)

**Linux:**
```bash
sudo apt-get install python3-pil
pip install Pillow
```

**macOS:**
```bash
brew install libjpeg
pip install Pillow
```

### Issue: Static Files Not Loading

1. Check STATIC_URL and STATIC_ROOT in settings.py
2. Run `python manage.py collectstatic`
3. Verify DEBUG=True for development

### Issue: Database Connection Error

1. Verify MySQL is running: `systemctl status mysql` (Linux) or check Services (Windows)
2. Test connection: `mysql -u petrescue_user -p`
3. Verify credentials in settings.py
4. Check database exists: `SHOW DATABASES;` in MySQL

### Issue: Port Already in Use

```bash
# Use different port
python manage.py runserver 8080

# Or find and kill process using port 8000
# Linux/macOS:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue: Permission Denied for Media Directory

**Linux/macOS:**
```bash
chmod -R 755 media/
chown -R $USER:$USER media/
```

**Windows:**
Right-click media folder → Properties → Security → Edit → Allow Full Control

## Environment Variables (Optional)

For better security, use environment variables:

1. Create `.env` file in project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=petrescue_db
DB_USER=petrescue_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

2. Update settings.py:
```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}
```

## Next Steps

After successful installation:

1. Read the [User Guide](README.md#usage-guide)
2. Explore the admin panel
3. Create test data (pets, requests)
4. Test all functionality
5. Configure for production if deploying

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review Django documentation: https://docs.djangoproject.com/
3. Check project README.md
4. Contact support: support@petrescue.com

## Production Deployment

For production deployment, additional steps required:

1. Set `DEBUG = False`
2. Configure `ALLOWED_HOSTS`
3. Use environment variables for secrets
4. Set up proper web server (Gunicorn, uWSGI)
5. Configure reverse proxy (Nginx, Apache)
6. Set up SSL certificate
7. Configure static file serving
8. Set up database backups
9. Enable logging
10. Configure email backend

See Django deployment documentation for details.
