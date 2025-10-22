from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import CustomUserRegistrationForm

User = get_user_model()

class CustomUserModelTest(TestCase):
    """Test cases for CustomUser model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            phone_number='+1234567890'
        )
    
    def test_user_creation(self):
        """Test user creation with custom fields"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.phone_number, '+1234567890')
        self.assertEqual(self.user.user_type, 'regular')
        self.assertFalse(self.user.is_verified)
    
    def test_user_str_method(self):
        """Test user string representation"""
        expected = f"{self.user.username} (Regular User)"
        self.assertEqual(str(self.user), expected)

class UserAuthenticationTest(TestCase):
    """Test cases for user authentication"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_login_view(self):
        """Test login view renders correctly"""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign in to your account')
    
    def test_register_view(self):
        """Test registration view renders correctly"""
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create your account')
    
    def test_successful_login(self):
        """Test successful user login"""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login
    
    def test_profile_requires_login(self):
        """Test profile view requires authentication"""
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

class UserRegistrationFormTest(TestCase):
    """Test cases for user registration form"""
    
    def test_valid_form(self):
        """Test form with valid data"""
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'new@example.com',
            'phone_number': '+1234567890',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = CustomUserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_password_mismatch(self):
        """Test form with mismatched passwords"""
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'complexpass123',
            'password2': 'differentpass123'
        }
        form = CustomUserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
