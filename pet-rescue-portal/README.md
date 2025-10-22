# PetRescue - Pet Adoption and Rescue Management Portal

## Project Overview

**PetRescue** is a comprehensive web-based platform designed to bridge the gap between individuals who find lost pets and their owners. The platform provides an intuitive interface for reporting lost or found pets, searching for pets, and managing reunion requests.

## Features

### Core Functionality
- **User Registration & Authentication**: Secure user accounts with profile management
- **Pet Reporting**: Users can report lost or found pets with detailed information and photos
- **Advanced Search**: Search functionality with multiple filters (type, status, size, location)
- **Pet Status Inquiry**: Check if your lost pet has been reported on the platform
- **Request Management**: Submit and track requests for pet reunions or adoptions
- **Notification System**: Receive updates on request status and potential pet matches
- **Comment System**: Add comments and additional information to pet reports
- **Admin Panel**: Administrative dashboard for managing requests and verifying pet reports

### User Roles
1. **Regular Users**: Can report pets, search for pets, submit requests, and manage their profiles
2. **Administrators**: Can verify pet reports, manage all requests, and access admin dashboard

## Technology Stack

- **Backend**: Django 4.2.7 (Python Web Framework)
- **Database**: MySQL 8.0+ (with SQLite option for development)
- **Frontend**: HTML5, CSS3 (Responsive Design)
- **Image Handling**: Pillow (Python Imaging Library)
- **Configuration Management**: python-decouple

## Project Structure

```
pet-rescue-portal/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── petrescue/               # Main project configuration
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── pets/                    # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── forms.py             # Form definitions
│   ├── urls.py              # App URL patterns
│   ├── admin.py             # Admin configuration
│   ├── apps.py              # App configuration
│   ├── static/              # Static files
│   │   ├── css/
│   │   │   └── style.css    # Main stylesheet
│   │   ├── js/
│   │   └── images/
│   └── templates/           # HTML templates
│       └── pets/
│           ├── base.html
│           ├── home.html
│           ├── login.html
│           ├── register.html
│           └── ...
└── media/                   # User uploaded files
    └── pet_photos/          # Pet photos
```

## Database Models

### 1. UserProfile
- Extended user profile with phone, address, and admin status
- One-to-one relationship with Django's User model

### 2. Pet
- Comprehensive pet information (type, breed, color, size, age)
- Physical characteristics and distinctive marks
- Status tracking (Lost, Found, Reunited, Adopted)
- Location and date information
- Contact details and photo upload
- Admin verification system

### 3. Request
- User requests for pet reunions or adoptions
- Request types: Found Pet, Lost Pet, Adoption Inquiry
- Status tracking (Pending, In Progress, Resolved, Rejected)
- Admin notes and response system

### 4. Notification
- User notifications for request updates and pet matches
- Different notification types
- Read/unread status tracking

### 5. Comment
- Comments on pet reports
- Community engagement and additional information sharing

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- MySQL 8.0+ (or use SQLite for development)
- pip (Python package manager)

### Step 1: Clone or Download the Project
```bash
cd /workspace/pet-rescue-portal
```

### Step 2: Create a Virtual Environment (Recommended)
```bash
python -m venv venv

# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Database Setup

#### Option A: Using MySQL (Recommended for Production)

1. Create a MySQL database:
```sql
CREATE DATABASE petrescue_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Update database settings in `petrescue/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'petrescue_db',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

#### Option B: Using SQLite (For Development/Testing)

Uncomment the SQLite configuration in `petrescue/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create a Superuser (Admin Account)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### Step 7: Create Media Directories
```bash
mkdir -p media/pet_photos
```

### Step 8: Run the Development Server
```bash
python manage.py runserver
```

The application will be available at: http://127.0.0.1:8000/

## Usage Guide

### For Regular Users

1. **Register an Account**
   - Click "Register" in the navigation menu
   - Fill out the registration form with your details
   - Login with your credentials

2. **Report a Lost Pet**
   - Click "Report Pet" in the navigation
   - Select "Lost" as the status
   - Fill in all pet details and upload a photo
   - Submit the report

3. **Report a Found Pet**
   - Click "Report Pet"
   - Select "Found" as the status
   - Provide all available information about the pet
   - Submit the report

4. **Search for Your Pet**
   - Go to "Find Pets"
   - Use search filters to narrow down results
   - Click on pet cards to view full details
   - Contact the reporter if you find a match

5. **Submit a Request**
   - Go to "My Requests"
   - Click "Create New Request"
   - Choose request type and provide details
   - Track your request status

### For Administrators

1. **Access Admin Panel**
   - Login with an admin account
   - Click "Admin Panel" in the navigation
   - View statistics and pending items

2. **Verify Pet Reports**
   - Review unverified pet reports
   - Click "Verify" to approve reports
   - Edit or delete inappropriate reports

3. **Manage Requests**
   - View all pending requests
   - Update request status
   - Add admin notes and responses
   - Mark requests as resolved or rejected

4. **Django Admin Interface**
   - Access at http://127.0.0.1:8000/admin/
   - Full control over all database records
   - User management and permissions

## Module Implementation

### Module 1: Database Design & User Management
✅ **Implemented**
- Complete database schema with 5 models
- User authentication and registration
- Profile management
- Admin user roles

### Module 2: Pet Registration & Admin Management
✅ **Implemented**
- Pet reporting functionality
- Photo upload capability
- Admin verification system
- Pet status management (Lost, Found, Reunited, Adopted)

### Module 3: Pet Status Inquiry & Notification
✅ **Implemented**
- Advanced search with multiple filters
- Detailed pet views with comments
- Notification system for updates
- Request tracking system

### Module 4: Testing, Review, and Documentation
✅ **Implemented**
- Comprehensive documentation
- Setup instructions
- User and admin guides
- Code comments and docstrings

## Configuration

### Important Settings

1. **SECRET_KEY**: Change in production
```python
SECRET_KEY = 'your-secret-key-here'
```

2. **DEBUG**: Set to False in production
```python
DEBUG = False
```

3. **ALLOWED_HOSTS**: Configure for production
```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

4. **Media and Static Files**
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_URL = '/static/'
```

## Security Considerations

- User passwords are hashed using Django's default password hashers
- CSRF protection enabled for all forms
- SQL injection protection through Django ORM
- XSS protection through template auto-escaping
- File upload validation for pet photos
- User authentication required for sensitive operations

## API Endpoints (URLs)

### Public Pages
- `/` - Home page
- `/about/` - About page
- `/contact/` - Contact page
- `/pets/` - Pet listing (search)
- `/pets/<id>/` - Pet detail page

### Authentication
- `/register/` - User registration
- `/login/` - User login
- `/logout/` - User logout
- `/profile/` - User profile

### Pet Management
- `/pets/report/` - Report a pet (requires login)
- `/pets/<id>/edit/` - Edit pet (requires login)
- `/pets/<id>/delete/` - Delete pet (requires login)

### Request Management
- `/requests/` - Request list (requires login)
- `/requests/create/` - Create request (requires login)
- `/requests/<id>/` - Request detail (requires login)

### Admin
- `/admin-panel/` - Admin dashboard (requires admin)
- `/admin/requests/<id>/update/` - Update request (requires admin)
- `/admin/pets/<id>/verify/` - Verify pet (requires admin)

### Notifications
- `/notifications/` - View notifications (requires login)

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check MySQL is running
   - Verify database credentials in settings.py
   - Ensure database exists

2. **Static Files Not Loading**
   ```bash
   python manage.py collectstatic
   ```

3. **Media Files Not Displaying**
   - Check MEDIA_ROOT and MEDIA_URL settings
   - Ensure media directories exist
   - Check file permissions

4. **Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

## Future Enhancements

- Email notifications for pet matches
- SMS alerts for urgent updates
- Geolocation-based search
- Pet matching algorithm
- Mobile application
- Social media integration
- Multi-language support
- Advanced analytics dashboard

## Support

For questions or issues:
- Email: support@petrescue.com
- Phone: (555) 123-4567

## License

This project is developed as an educational project for learning Django web development.

## Contributors

- Development Team
- Academic Institution

## Acknowledgments

- Django Documentation
- Bootstrap/CSS Framework
- Pet welfare organizations for inspiration

---

**Note**: This is a educational project. For production deployment, additional security hardening, performance optimization, and testing would be required.
