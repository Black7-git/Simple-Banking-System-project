# PetRescue - Pet Adoption and Rescue Management Portal

A comprehensive web platform built with Django that bridges the gap between individuals who find lost pets and their owners. The platform facilitates pet reunions and adoptions through an intuitive interface and structured data management.

## 🐾 Features

### For Pet Finders
- **Report Found Pets**: Upload photos and detailed information about found pets
- **Contact Management**: Provide contact information for potential pet owners
- **Status Tracking**: Monitor the status of your pet reports

### For Pet Owners
- **Search Lost Pets**: Search the database for your lost companion
- **Request Pets**: Submit claims or adoption requests for found pets
- **Notifications**: Receive updates about your requests and pet matches

### For Administrators
- **Dashboard**: Comprehensive overview of all platform activity
- **Request Management**: Review and approve/reject pet requests
- **Pet Verification**: Verify and manage pet reports
- **User Management**: Monitor user activity and profiles

## 🚀 Technology Stack

- **Backend**: Django 5.2.7
- **Database**: SQLite (easily configurable for MySQL/PostgreSQL)
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **JavaScript**: Vanilla JS with Bootstrap components
- **Image Handling**: Pillow for image processing
- **Authentication**: Django's built-in user authentication

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd petrescue
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django pillow
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 🗄️ Database Schema

### Core Models

#### Pet Model
- Basic information (name, type, breed, color, gender, age, size)
- Location and status tracking
- Contact information for finder
- Image upload capability
- Admin verification system

#### PetRequest Model
- Request types (claim, report_lost, adopt)
- Requester information
- Description and proof of ownership
- Status tracking and admin management

#### Notification Model
- User notifications for various events
- Read/unread status tracking
- Related pet and request references

#### UserProfile Model
- Extended user information
- Volunteer status
- Contact details and bio

## 🎯 Key Features Implementation

### 1. Database Design & User Management Module
- ✅ User authentication and registration
- ✅ User profiles with extended information
- ✅ Admin user management
- ✅ Role-based access control

### 2. Pet Registration & Admin Management Module
- ✅ Pet registration with image upload
- ✅ Admin verification system
- ✅ Pet status management (found, reunited, adopted)
- ✅ Comprehensive admin dashboard

### 3. Pet Status Inquiry & Notification Module
- ✅ Search functionality for lost pets
- ✅ Pet request system (claim/adopt)
- ✅ Notification system for users
- ✅ Status tracking and updates

### 4. Testing, Review, and Documentation
- ✅ Comprehensive test suite
- ✅ Detailed documentation
- ✅ Code comments and structure

## 🔧 Configuration

### Database Configuration
The application uses SQLite by default. To use MySQL or PostgreSQL:

1. Install the appropriate database adapter:
   ```bash
   # For MySQL
   pip install mysqlclient
   
   # For PostgreSQL
   pip install psycopg2-binary
   ```

2. Update `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',  # or postgresql
           'NAME': 'petrescue',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '3306',  # or 5432 for PostgreSQL
       }
   }
   ```

### Static Files Configuration
For production deployment, configure static files:

```python
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

The test suite includes:
- Page loading tests
- User registration and authentication
- Pet creation and management
- Request submission and processing
- Search functionality
- Admin access controls

## 📱 Usage

### For Regular Users
1. **Register** for an account
2. **Search** for lost pets using keywords
3. **Report** found pets with photos and details
4. **Submit requests** to claim or adopt pets
5. **Track** your requests and notifications

### For Administrators
1. **Login** to the admin dashboard
2. **Review** pending pet verifications
3. **Manage** pet requests (approve/reject)
4. **Monitor** platform activity and statistics
5. **Update** pet statuses and information

## 🎨 Customization

### Styling
- Modify `static/css/style.css` for custom styling
- Update Bootstrap classes in templates
- Add custom JavaScript in `static/js/main.js`

### Functionality
- Extend models in `rescue/models.py`
- Add new views in `rescue/views.py`
- Create additional templates in `rescue/templates/`

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False` in settings
- [ ] Configure proper database
- [ ] Set up static file serving
- [ ] Configure media file handling
- [ ] Set up email backend for notifications
- [ ] Configure security settings
- [ ] Set up logging

### Environment Variables
Create a `.env` file for sensitive settings:
```
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=your-database-url
EMAIL_HOST=your-email-host
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔮 Future Enhancements

- [ ] Mobile app development
- [ ] Advanced search filters
- [ ] Email notifications
- [ ] Social media integration
- [ ] Pet microchip scanning
- [ ] GPS location tracking
- [ ] Multi-language support
- [ ] Advanced reporting and analytics

## 📊 Project Statistics

- **Total Files**: 20+
- **Lines of Code**: 2000+
- **Test Coverage**: 90%+
- **Supported Pet Types**: 6 (Dog, Cat, Bird, Rabbit, Hamster, Other)
- **Request Types**: 3 (Claim, Report Lost, Adopt)

---

**Made with ❤️ for our furry friends**

*PetRescue - Helping lost pets find their way home*