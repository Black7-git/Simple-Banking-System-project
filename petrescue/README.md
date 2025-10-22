# PetRescue - Pet Adoption and Rescue Management Portal

A comprehensive web platform that bridges the gap between individuals who find lost pets and their owners, facilitating reunions through community support and advanced matching technology.

## 🎯 Project Overview

**PetRescue** is an interactive web platform designed to help reunite lost pets with their families. The website provides functionalities for users to report found pets, search for lost pets, and manage requests to facilitate successful reunions.

### Key Features

- **Pet Registration & Management**: Report found or lost pets with detailed descriptions and photos
- **Advanced Search System**: Search pets by type, location, color, size, and other attributes
- **User Authentication**: Secure user registration and login system with profile management
- **Admin Panel**: Comprehensive admin interface for managing pets, users, and requests
- **Notification System**: Real-time notifications for potential matches and updates
- **Responsive Design**: Modern, mobile-friendly interface built with Bootstrap 5

## 🛠 Technology Stack

- **Backend**: Django 5.2.7 (Python)
- **Database**: SQLite (easily configurable for MySQL/PostgreSQL)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Image Handling**: Pillow for image processing
- **Authentication**: Django's built-in authentication system with custom user model

## 📁 Project Structure

```
petrescue/
├── accounts/              # User management app
│   ├── models.py         # Custom user model
│   ├── forms.py          # User registration and profile forms
│   ├── views.py          # Authentication views
│   └── admin.py          # User admin configuration
├── pets/                 # Pet management app
│   ├── models.py         # Pet, PetImage, PetRequest models
│   ├── forms.py          # Pet reporting and search forms
│   ├── views.py          # Pet CRUD and search views
│   └── admin.py          # Pet admin configuration
├── notifications/        # Notification system
│   ├── models.py         # Notification and PetMatch models
│   ├── views.py          # Notification management views
│   └── admin.py          # Notification admin configuration
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── accounts/         # Authentication templates
│   ├── pets/             # Pet-related templates
│   └── notifications/    # Notification templates
├── static/               # Static files (CSS, JS, images)
├── media/                # User-uploaded files
└── requirements.txt      # Python dependencies
```

## 🚀 Installation and Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd petrescue
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 👥 User Roles and Permissions

### Regular Users
- Register and manage their profile
- Report found or lost pets
- Search and browse pet listings
- Submit requests to contact pet owners/finders
- Receive notifications about potential matches

### Administrators
- Access to Django admin panel
- Verify and manage pet reports
- Review and respond to user requests
- Manage user accounts and permissions
- Monitor system activity and generate reports

## 📊 Database Models

### CustomUser
Extended Django user model with additional fields:
- User type (regular/admin)
- Phone number and address
- Profile picture
- Verification status

### Pet
Core model for pet information:
- Basic info (name, type, breed, color, size, age, gender)
- Physical description and distinctive features
- Location and date information
- Status (found/lost/reunited/adopted)
- Contact information

### PetImage
Multiple images per pet with captions

### PetRequest
User requests for pet inquiries and adoption

### Notification
System notifications for users

### PetMatch
Potential matches between found and lost pets

## 🔧 Configuration

### Database Configuration
The project uses SQLite by default. To use MySQL or PostgreSQL:

1. Install the appropriate database adapter:
   ```bash
   pip install mysqlclient  # for MySQL
   pip install psycopg2     # for PostgreSQL
   ```

2. Update `DATABASES` setting in `settings.py`

### Media Files
Configure `MEDIA_ROOT` and `MEDIA_URL` in settings for file uploads.

### Email Configuration
For production, configure email settings for notifications:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your-smtp-server.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@domain.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 📱 API Endpoints

### Main URLs
- `/` - Home page
- `/pets/` - Pet listings with search
- `/pets/<id>/` - Pet detail page
- `/report/` - Report a pet form
- `/accounts/login/` - User login
- `/accounts/register/` - User registration
- `/accounts/profile/` - User profile
- `/notifications/` - User notifications
- `/admin/` - Admin panel

## 🎨 UI/UX Features

- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Modern Interface**: Clean, intuitive design with Bootstrap 5
- **Image Gallery**: Carousel display for multiple pet photos
- **Search Filters**: Advanced filtering options for pet search
- **Status Badges**: Visual indicators for pet status
- **Social Sharing**: Share pet listings on social media

## 🔒 Security Features

- CSRF protection on all forms
- User authentication and authorization
- Input validation and sanitization
- Secure file upload handling
- Admin-only access to sensitive operations

## 📈 Future Enhancements

- **Geolocation Integration**: Map-based search and location services
- **SMS Notifications**: Text message alerts for urgent matches
- **Mobile App**: Native iOS and Android applications
- **AI Matching**: Machine learning for better pet matching
- **Multi-language Support**: Internationalization for global use
- **Payment Integration**: Donation and adoption fee processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation wiki

## 🙏 Acknowledgments

- Django community for the excellent framework
- Bootstrap team for the responsive CSS framework
- Contributors and testers who helped improve the platform

---

**PetRescue** - Reuniting pets with their families through technology and community support.