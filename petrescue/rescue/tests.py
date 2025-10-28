from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Pet, PetRequest, Notification, UserProfile


class PetRescueTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test pet
        self.pet = Pet.objects.create(
            name='Buddy',
            pet_type='dog',
            breed='Golden Retriever',
            color='Golden',
            gender='male',
            age=3,
            size='large',
            location_found='Central Park',
            description='Friendly golden retriever found near the pond',
            finder_name='John Doe',
            finder_phone='+1234567890',
            finder_email='john@example.com',
            created_by=self.user
        )
        
        # Create test request
        self.request = PetRequest.objects.create(
            request_type='claim',
            pet=self.pet,
            requester_name='Jane Smith',
            requester_phone='+0987654321',
            requester_email='jane@example.com',
            description='This is my lost dog Buddy',
            proof_of_ownership='He has a blue collar and responds to his name'
        )

    def test_home_page(self):
        """Test home page loads correctly"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PetRescue')

    def test_pet_list_page(self):
        """Test pet list page loads correctly"""
        response = self.client.get(reverse('pet_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Found Pets')

    def test_pet_detail_page(self):
        """Test pet detail page loads correctly"""
        response = self.client.get(reverse('pet_detail', args=[self.pet.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.pet.name)

    def test_report_pet_page(self):
        """Test report pet page loads correctly"""
        response = self.client.get(reverse('report_pet'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Report Found Pet')

    def test_search_lost_pet_page(self):
        """Test search lost pet page loads correctly"""
        response = self.client.get(reverse('search_lost_pet'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Search for Your Lost Pet')

    def test_register_page(self):
        """Test registration page loads correctly"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Account')

    def test_pet_creation(self):
        """Test pet creation"""
        self.assertEqual(Pet.objects.count(), 1)
        self.assertEqual(self.pet.name, 'Buddy')
        self.assertEqual(self.pet.pet_type, 'dog')

    def test_pet_request_creation(self):
        """Test pet request creation"""
        self.assertEqual(PetRequest.objects.count(), 1)
        self.assertEqual(self.request.request_type, 'claim')
        self.assertEqual(self.request.requester_name, 'Jane Smith')

    def test_user_registration(self):
        """Test user registration"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_pet_search(self):
        """Test pet search functionality"""
        response = self.client.post(reverse('search_lost_pet'), {
            'search_query': 'Buddy'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Buddy')

    def test_pet_request_form(self):
        """Test pet request form submission"""
        response = self.client.post(reverse('request_pet', args=[self.pet.id]), {
            'request_type': 'adopt',
            'requester_name': 'Test Requester',
            'requester_phone': '+1111111111',
            'requester_email': 'test@example.com',
            'description': 'I would like to adopt this pet',
            'proof_of_ownership': ''
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful submission
        self.assertEqual(PetRequest.objects.count(), 2)  # Original + new request

    def test_admin_access_required(self):
        """Test that admin pages require authentication"""
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_authenticated_user_access(self):
        """Test authenticated user can access profile"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profile Information')

    def test_pet_model_str(self):
        """Test pet model string representation"""
        expected = f"{self.pet.pet_type.title()} - {self.pet.location_found} ({self.pet.status})"
        self.assertEqual(str(self.pet), expected)

    def test_pet_request_model_str(self):
        """Test pet request model string representation"""
        expected = f"{self.request.request_type} for {self.request.pet} by {self.request.requester_name}"
        self.assertEqual(str(self.request), expected)