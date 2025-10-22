from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date
from .models import Pet, PetImage, PetRequest
from .forms import PetReportForm, PetSearchForm

User = get_user_model()

class PetModelTest(TestCase):
    """Test cases for Pet model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.pet = Pet.objects.create(
            name='Buddy',
            pet_type='dog',
            breed='Golden Retriever',
            color='Golden',
            size='large',
            description='Friendly dog found in park',
            status='found',
            found_location='Central Park',
            found_date=date.today(),
            reported_by=self.user,
            contact_phone='+1234567890',
            contact_email='test@example.com'
        )
    
    def test_pet_creation(self):
        """Test pet creation with required fields"""
        self.assertEqual(self.pet.name, 'Buddy')
        self.assertEqual(self.pet.pet_type, 'dog')
        self.assertEqual(self.pet.status, 'found')
        self.assertEqual(self.pet.reported_by, self.user)
        self.assertFalse(self.pet.is_verified)
    
    def test_pet_str_method(self):
        """Test pet string representation"""
        expected = "Buddy - Dog (Found Pet)"
        self.assertEqual(str(self.pet), expected)

class PetViewsTest(TestCase):
    """Test cases for pet views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.pet = Pet.objects.create(
            name='Buddy',
            pet_type='dog',
            breed='Golden Retriever',
            color='Golden',
            size='large',
            description='Friendly dog found in park',
            status='found',
            found_location='Central Park',
            found_date=date.today(),
            reported_by=self.user,
            contact_phone='+1234567890',
            contact_email='test@example.com',
            is_verified=True
        )
    
    def test_home_view(self):
        """Test home page renders correctly"""
        response = self.client.get(reverse('pets:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reuniting Pets with Their Families')
    
    def test_pet_list_view(self):
        """Test pet list view"""
        response = self.client.get(reverse('pets:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Buddy')
    
    def test_pet_detail_view(self):
        """Test pet detail view"""
        response = self.client.get(reverse('pets:detail', args=[self.pet.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Buddy')
        self.assertContains(response, 'Golden Retriever')
    
    def test_report_pet_requires_login(self):
        """Test report pet view requires authentication"""
        response = self.client.get(reverse('pets:report'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_pet_search(self):
        """Test pet search functionality"""
        response = self.client.get(reverse('pets:list'), {'query': 'Buddy'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Buddy')

class PetFormsTest(TestCase):
    """Test cases for pet forms"""
    
    def test_pet_report_form_valid(self):
        """Test pet report form with valid data"""
        form_data = {
            'name': 'Max',
            'pet_type': 'dog',
            'breed': 'Labrador',
            'color': 'Black',
            'size': 'large',
            'gender': 'male',
            'description': 'Friendly black lab',
            'status': 'found',
            'found_location': 'Main Street',
            'found_date': date.today().strftime('%Y-%m-%d'),
            'contact_phone': '+1234567890',
            'contact_email': 'test@example.com'
        }
        form = PetReportForm(data=form_data)
        if not form.is_valid():
            print("Form errors:", form.errors)
        self.assertTrue(form.is_valid())
    
    def test_pet_search_form(self):
        """Test pet search form"""
        form_data = {
            'query': 'dog',
            'pet_type': 'dog',
            'status': 'found'
        }
        form = PetSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

class PetRequestTest(TestCase):
    """Test cases for PetRequest model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.pet = Pet.objects.create(
            name='Buddy',
            pet_type='dog',
            color='Golden',
            size='large',
            status='found',
            found_location='Park',
            found_date=date.today(),
            reported_by=self.user,
            contact_phone='+1234567890',
            contact_email='test@example.com'
        )
        self.request = PetRequest.objects.create(
            request_type='lost_inquiry',
            pet=self.pet,
            requester=self.user,
            message='I think this is my lost dog'
        )
    
    def test_pet_request_creation(self):
        """Test pet request creation"""
        self.assertEqual(self.request.request_type, 'lost_inquiry')
        self.assertEqual(self.request.pet, self.pet)
        self.assertEqual(self.request.requester, self.user)
        self.assertEqual(self.request.status, 'pending')
    
    def test_pet_request_str_method(self):
        """Test pet request string representation"""
        expected = "Lost Pet Inquiry by testuser"
        self.assertEqual(str(self.request), expected)
