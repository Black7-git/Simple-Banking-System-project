# PetRescue Project Structure

This document describes the complete structure of the PetRescue project.

## Directory Tree

```
pet-rescue-portal/
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── setup.py                       # Automated setup script
├── .gitignore                     # Git ignore patterns
│
├── README.md                      # Main project documentation
├── INSTALLATION.md                # Detailed installation guide
├── QUICK_START.md                 # Quick setup instructions
├── TESTING.md                     # Testing procedures and test cases
├── PROJECT_STRUCTURE.md           # This file
│
├── petrescue/                     # Main Django project configuration
│   ├── __init__.py               # Python package marker
│   ├── settings.py               # Django settings and configuration
│   ├── urls.py                   # Main URL routing
│   ├── wsgi.py                   # WSGI application
│   └── asgi.py                   # ASGI application
│
├── pets/                          # Main application
│   ├── __init__.py               # Python package marker
│   ├── apps.py                   # App configuration
│   ├── models.py                 # Database models
│   ├── views.py                  # View functions
│   ├── urls.py                   # App URL patterns
│   ├── forms.py                  # Form definitions
│   ├── admin.py                  # Django admin configuration
│   │
│   ├── static/                   # Static files
│   │   ├── css/
│   │   │   └── style.css        # Main stylesheet
│   │   ├── js/                   # JavaScript files (empty for now)
│   │   └── images/               # Static images (empty for now)
│   │
│   └── templates/                # HTML templates
│       └── pets/
│           ├── base.html         # Base template with navigation
│           ├── home.html         # Homepage
│           ├── about.html        # About page
│           ├── contact.html      # Contact page
│           │
│           ├── login.html        # User login
│           ├── register.html     # User registration
│           ├── profile.html      # User profile
│           │
│           ├── pet_list.html     # Pet search/listing
│           ├── pet_detail.html   # Pet details
│           ├── report_pet.html   # Report pet form
│           ├── edit_pet.html     # Edit pet form
│           ├── delete_pet.html   # Delete confirmation
│           │
│           ├── request_list.html       # Request listing
│           ├── request_detail.html     # Request details
│           ├── create_request.html     # Create request form
│           │
│           ├── notifications.html      # User notifications
│           │
│           ├── admin_panel.html        # Admin dashboard
│           └── admin_update_request.html # Admin request update
│
└── media/                         # User uploaded files
    └── pet_photos/               # Pet photos directory
```

## File Descriptions

### Root Level Files

#### manage.py
- Django's command-line utility
- Used for running server, migrations, creating users, etc.
- Usage: `python manage.py <command>`

#### requirements.txt
- Lists all Python dependencies
- Install with: `pip install -r requirements.txt`
- Dependencies:
  - Django 4.2.7
  - mysqlclient 2.2.0
  - Pillow 10.1.0
  - python-decouple 3.8

#### setup.py
- Automated setup script
- Installs dependencies and sets up database
- Usage: `python setup.py`

#### .gitignore
- Specifies files to ignore in Git
- Excludes: venv/, *.pyc, db.sqlite3, media/, etc.

### Documentation Files

#### README.md
- Main project documentation
- Features overview
- Installation instructions
- Usage guide
- Module implementation details

#### INSTALLATION.md
- Detailed installation guide
- Step-by-step setup instructions
- Database configuration
- Troubleshooting tips
- Production deployment notes

#### QUICK_START.md
- Quick 5-minute setup guide
- Minimal steps to get started
- Basic troubleshooting

#### TESTING.md
- Comprehensive testing guide
- Manual test cases
- User acceptance testing scenarios
- Bug reporting template

#### PROJECT_STRUCTURE.md
- This file
- Project structure documentation
- File descriptions
- Module organization

### Django Configuration (petrescue/)

#### settings.py
**Purpose**: Main Django configuration
**Key Settings**:
- Database configuration (MySQL/SQLite)
- Installed apps
- Middleware
- Templates configuration
- Static and media files settings
- Authentication settings

**Important Configurations**:
```python
DATABASES = {...}          # Database settings
INSTALLED_APPS = [...]     # Registered applications
STATIC_URL = '/static/'    # Static files URL
MEDIA_URL = '/media/'      # Media files URL
```

#### urls.py
**Purpose**: Main URL routing
**Routes**:
- `/admin/` - Django admin interface
- `/` - All app URLs (delegated to pets.urls)
- Media file serving (development only)

#### wsgi.py & asgi.py
**Purpose**: Web server interfaces
- WSGI: Standard synchronous interface
- ASGI: Asynchronous interface (for future features)

### Application Files (pets/)

#### models.py
**Purpose**: Database model definitions
**Models**:
1. **UserProfile**: Extended user information
   - Fields: user, phone, address, is_admin
   - Relationship: OneToOne with User

2. **Pet**: Pet information
   - Fields: name, type, breed, color, size, status, location, date, photo, etc.
   - Relationships: ForeignKey to User (reported_by, verified_by)

3. **Request**: User requests
   - Fields: type, subject, description, status, admin_notes
   - Relationships: ForeignKey to User and Pet

4. **Notification**: User notifications
   - Fields: type, title, message, is_read
   - Relationships: ForeignKey to User, Pet, Request

5. **Comment**: Pet report comments
   - Fields: content, created_at
   - Relationships: ForeignKey to User and Pet

#### views.py
**Purpose**: Business logic and view functions
**Main Views**:
- Authentication: register, user_login, user_logout, profile
- Pet Management: pet_list, pet_detail, report_pet, edit_pet, delete_pet
- Request Management: request_list, request_detail, create_request
- Admin: admin_panel, admin_update_request, admin_verify_pet
- Notifications: notifications
- Static Pages: home, about, contact

#### forms.py
**Purpose**: Form definitions
**Forms**:
- UserRegistrationForm: User registration
- UserProfileForm: Profile updates
- PetReportForm: Pet reporting
- PetSearchForm: Search filters
- RequestForm: Request creation
- AdminRequestUpdateForm: Admin request management
- CommentForm: Pet comments

#### urls.py
**Purpose**: App-specific URL routing
**URL Patterns**:
- Home and static pages
- Authentication URLs
- Pet management URLs
- Request management URLs
- Admin URLs
- Notification URLs

#### admin.py
**Purpose**: Django admin interface configuration
**Registered Models**:
- UserProfile (with custom display)
- Pet (with detailed fieldsets)
- Request (with filtering options)
- Notification (with read status)
- Comment (with timestamp)

### Static Files (pets/static/)

#### css/style.css
**Purpose**: Main stylesheet
**Sections**:
- CSS variables for colors
- Reset and base styles
- Navigation styling
- Component styles (buttons, forms, cards)
- Responsive design media queries
- Utility classes

**Key Features**:
- Modern, clean design
- Responsive layout
- Custom color scheme
- Professional typography
- Smooth transitions

#### js/ (empty)
- Reserved for future JavaScript files
- Can add interactive features like:
  - Form validation
  - Dynamic search
  - Image preview
  - Real-time notifications

#### images/ (empty)
- Reserved for static images
- Can add:
  - Logo
  - Icons
  - Background images
  - Placeholder images

### Templates (pets/templates/pets/)

#### base.html
**Purpose**: Base template for all pages
**Features**:
- Navigation bar
- User authentication menu
- Message display
- Footer
- Common structure

#### Authentication Templates
- **login.html**: User login form
- **register.html**: User registration with profile fields
- **profile.html**: User profile and dashboard

#### Pet Management Templates
- **pet_list.html**: Search and browse pets with filters
- **pet_detail.html**: Detailed pet information and comments
- **report_pet.html**: Form to report lost/found pets
- **edit_pet.html**: Edit existing pet reports
- **delete_pet.html**: Confirmation page for deletion

#### Request Templates
- **request_list.html**: List of user requests
- **request_detail.html**: Detailed request view
- **create_request.html**: Form to create new request

#### Admin Templates
- **admin_panel.html**: Admin dashboard with statistics
- **admin_update_request.html**: Form to update request status

#### Notification Templates
- **notifications.html**: User notification center

#### Static Pages
- **home.html**: Homepage with recent pets and statistics
- **about.html**: About PetRescue
- **contact.html**: Contact information and FAQ

### Media Files (media/)

#### pet_photos/
**Purpose**: Stores uploaded pet photos
**Characteristics**:
- User-uploaded content
- Managed by Django
- Accessible via MEDIA_URL
- Should be excluded from Git

## Module Organization

### Module 1: Database Design & User Management
**Files**:
- `pets/models.py` - UserProfile model
- `pets/views.py` - register, login, logout, profile views
- `pets/forms.py` - UserRegistrationForm, UserProfileForm
- Templates: register.html, login.html, profile.html

### Module 2: Pet Registration & Admin Management
**Files**:
- `pets/models.py` - Pet model
- `pets/views.py` - report_pet, edit_pet, delete_pet, admin_verify_pet
- `pets/forms.py` - PetReportForm
- `pets/admin.py` - PetAdmin configuration
- Templates: report_pet.html, edit_pet.html, delete_pet.html, admin_panel.html

### Module 3: Pet Status Inquiry & Notification
**Files**:
- `pets/models.py` - Request, Notification models
- `pets/views.py` - pet_list, pet_detail, create_request, notifications
- `pets/forms.py` - PetSearchForm, RequestForm
- Templates: pet_list.html, pet_detail.html, notifications.html, create_request.html

### Module 4: Testing, Review, and Documentation
**Files**:
- README.md
- INSTALLATION.md
- TESTING.md
- QUICK_START.md
- PROJECT_STRUCTURE.md
- Code comments and docstrings

## Data Flow

### User Registration Flow
1. User accesses `/register/`
2. Fills UserRegistrationForm
3. View creates User and UserProfile
4. User logged in automatically
5. Redirected to home page

### Pet Reporting Flow
1. User accesses `/pets/report/`
2. Fills PetReportForm with details and photo
3. View creates Pet instance
4. Photo saved to media/pet_photos/
5. Redirected to pet detail page

### Search Flow
1. User accesses `/pets/`
2. Fills search filters
3. View filters Pet queryset
4. Results displayed in grid
5. Pagination handles large results

### Request Management Flow
1. User creates request
2. Request marked as "Pending"
3. Admin views in admin panel
4. Admin updates status and adds notes
5. Notification created for user
6. User views notification

## Database Schema

### Key Relationships
```
User (Django built-in)
  ├─ OneToOne: UserProfile
  ├─ ForeignKey (many): Pet.reported_by
  ├─ ForeignKey (many): Pet.verified_by
  ├─ ForeignKey (many): Request.requester
  ├─ ForeignKey (many): Request.resolved_by
  ├─ ForeignKey (many): Notification.user
  └─ ForeignKey (many): Comment.user

Pet
  ├─ ForeignKey: User (reported_by)
  ├─ ForeignKey: User (verified_by)
  ├─ ForeignKey (many): Request.pet
  ├─ ForeignKey (many): Notification.related_pet
  └─ ForeignKey (many): Comment.pet

Request
  ├─ ForeignKey: User (requester)
  ├─ ForeignKey: User (resolved_by)
  ├─ ForeignKey: Pet
  └─ ForeignKey (many): Notification.related_request

Notification
  ├─ ForeignKey: User
  ├─ ForeignKey: Pet (optional)
  └─ ForeignKey: Request (optional)

Comment
  ├─ ForeignKey: User
  └─ ForeignKey: Pet
```

## Configuration Files

### settings.py Key Settings

```python
# Database
DATABASES = {...}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'pets' / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Authentication
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
```

## Security Features

1. **Authentication**: Django's built-in auth system
2. **CSRF Protection**: Enabled on all forms
3. **Password Hashing**: Django default (PBKDF2)
4. **SQL Injection**: Protected via ORM
5. **XSS Protection**: Template auto-escaping
6. **File Upload Validation**: Via Pillow
7. **Permission Checks**: Login required decorators

## Future Enhancements

### Potential Additions
- `pets/api.py` - REST API endpoints
- `pets/serializers.py` - API serializers
- `pets/tests.py` - Automated tests
- `pets/utils.py` - Utility functions
- `pets/signals.py` - Django signals
- `pets/management/commands/` - Custom management commands

### Additional Templates
- Email templates for notifications
- PDF generation for reports
- Print-friendly views

### Additional Static Files
- JavaScript for dynamic features
- Additional CSS for themes
- Icons and branding

## Maintenance

### Regular Tasks
1. Database backups
2. Media file management
3. Log file rotation
4. Security updates
5. Performance monitoring

### Development Workflow
1. Edit code in appropriate files
2. Test changes locally
3. Run migrations if models changed
4. Collect static files if CSS/JS changed
5. Update documentation
6. Commit to version control

## Conclusion

This structure provides a solid foundation for a pet rescue management system. The modular organization makes it easy to maintain and extend with new features.
