#!/usr/bin/env python
"""
Script to create sample data for PetRescue application.
Run this script to populate the database with test data for demonstration purposes.

Usage:
    python manage.py shell < create_sample_data.py
"""

from datetime import date, timedelta
from django.contrib.auth import get_user_model
from pets.models import Pet, PetRequest
from notifications.models import Notification
import random

User = get_user_model()

# Create sample users
print("Creating sample users...")

# Create regular users
users_data = [
    {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe', 'phone_number': '+1234567890'},
    {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith', 'phone_number': '+1234567891'},
    {'username': 'mike_wilson', 'email': 'mike@example.com', 'first_name': 'Mike', 'last_name': 'Wilson', 'phone_number': '+1234567892'},
    {'username': 'sarah_jones', 'email': 'sarah@example.com', 'first_name': 'Sarah', 'last_name': 'Jones', 'phone_number': '+1234567893'},
    {'username': 'david_brown', 'email': 'david@example.com', 'first_name': 'David', 'last_name': 'Brown', 'phone_number': '+1234567894'},
]

created_users = []
for user_data in users_data:
    user, created = User.objects.get_or_create(
        username=user_data['username'],
        defaults={
            'email': user_data['email'],
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'phone_number': user_data['phone_number'],
            'is_verified': True
        }
    )
    if created:
        user.set_password('password123')
        user.save()
        print(f"Created user: {user.username}")
    created_users.append(user)

# Create sample pets
print("\nCreating sample pets...")

pets_data = [
    {
        'name': 'Buddy',
        'pet_type': 'dog',
        'breed': 'Golden Retriever',
        'color': 'Golden',
        'size': 'large',
        'gender': 'male',
        'age_estimate': '3-4 years',
        'description': 'Very friendly golden retriever. Loves playing fetch and is great with kids. Has a slight limp on left front paw.',
        'distinctive_features': 'Small scar above left eye, red collar with bell',
        'status': 'found',
        'found_location': 'Central Park, near the playground',
        'current_location': 'Safe at my home',
        'found_date': date.today() - timedelta(days=2),
        'is_verified': True
    },
    {
        'name': 'Whiskers',
        'pet_type': 'cat',
        'breed': 'Persian',
        'color': 'White and gray',
        'size': 'medium',
        'gender': 'female',
        'age_estimate': '2-3 years',
        'description': 'Beautiful long-haired Persian cat. Very calm and gentle. Appears to be well-cared for.',
        'distinctive_features': 'Blue eyes, pink rhinestone collar',
        'status': 'found',
        'found_location': 'Main Street, outside grocery store',
        'current_location': 'Local animal shelter',
        'found_date': date.today() - timedelta(days=5),
        'is_verified': True
    },
    {
        'name': 'Max',
        'pet_type': 'dog',
        'breed': 'German Shepherd',
        'color': 'Black and tan',
        'size': 'large',
        'gender': 'male',
        'age_estimate': '5-6 years',
        'description': 'Large German Shepherd, well-trained and obedient. Responds to basic commands.',
        'distinctive_features': 'Notched left ear, blue collar with ID tag (unreadable)',
        'status': 'lost',
        'found_location': 'Last seen near Oak Street Park',
        'current_location': '',
        'found_date': date.today() - timedelta(days=1),
        'is_verified': True
    },
    {
        'name': 'Luna',
        'pet_type': 'cat',
        'breed': 'Siamese',
        'color': 'Cream and brown',
        'size': 'small',
        'gender': 'female',
        'age_estimate': '1-2 years',
        'description': 'Young Siamese cat, very vocal and active. Indoor cat that got outside.',
        'distinctive_features': 'Bright blue eyes, small chip in left ear',
        'status': 'lost',
        'found_location': 'Elm Street neighborhood',
        'current_location': '',
        'found_date': date.today() - timedelta(days=3),
        'is_verified': True
    },
    {
        'name': 'Charlie',
        'pet_type': 'dog',
        'breed': 'Beagle',
        'color': 'Brown, black and white',
        'size': 'medium',
        'gender': 'male',
        'age_estimate': '4-5 years',
        'description': 'Friendly beagle with excellent temperament. Loves treats and belly rubs.',
        'distinctive_features': 'White patch on chest, brown leather collar',
        'status': 'reunited',
        'found_location': 'Downtown area',
        'current_location': 'Reunited with family',
        'found_date': date.today() - timedelta(days=7),
        'is_verified': True
    },
    {
        'name': '',
        'pet_type': 'bird',
        'breed': 'Cockatiel',
        'color': 'Gray and yellow',
        'size': 'small',
        'gender': 'unknown',
        'age_estimate': 'Adult',
        'description': 'Beautiful cockatiel found in backyard. Appears tame and used to human contact.',
        'distinctive_features': 'Yellow crest feathers, can whistle simple tunes',
        'status': 'found',
        'found_location': 'Residential area on Pine Street',
        'current_location': 'Temporary care at finder\'s home',
        'found_date': date.today() - timedelta(days=4),
        'is_verified': True
    }
]

created_pets = []
for i, pet_data in enumerate(pets_data):
    user = created_users[i % len(created_users)]
    pet_data['reported_by'] = user
    pet_data['contact_phone'] = user.phone_number
    pet_data['contact_email'] = user.email
    
    pet, created = Pet.objects.get_or_create(
        name=pet_data['name'],
        pet_type=pet_data['pet_type'],
        breed=pet_data['breed'],
        defaults=pet_data
    )
    if created:
        print(f"Created pet: {pet.name or 'Unnamed ' + pet.get_pet_type_display()}")
    created_pets.append(pet)

# Create sample pet requests
print("\nCreating sample pet requests...")

request_messages = [
    "I think this might be my lost dog! The description matches perfectly. Can we arrange a meeting?",
    "This looks exactly like my neighbor's missing cat. I'll let them know right away.",
    "I'm interested in adopting this pet if no owner is found. Please let me know the process.",
    "I saw this pet in my neighborhood yesterday. It might still be in the area.",
    "This is definitely my pet! I can provide proof of ownership. Please contact me ASAP."
]

for i in range(8):
    requester = random.choice(created_users)
    pet = random.choice(created_pets)
    
    # Don't create request if user is the reporter
    if requester != pet.reported_by:
        request_type = random.choice(['lost_inquiry', 'found_report', 'adoption_request'])
        message = random.choice(request_messages)
        
        pet_request, created = PetRequest.objects.get_or_create(
            request_type=request_type,
            pet=pet,
            requester=requester,
            defaults={
                'message': message,
                'status': random.choice(['pending', 'approved', 'completed'])
            }
        )
        if created:
            print(f"Created request: {pet_request.get_request_type_display()} for {pet.name or 'unnamed pet'}")

# Create sample notifications
print("\nCreating sample notifications...")

notification_data = [
    {
        'title': 'New Pet Match Found!',
        'message': 'We found a potential match for your lost pet. Check your requests for more details.',
        'notification_type': 'pet_match'
    },
    {
        'title': 'Request Status Updated',
        'message': 'Your pet inquiry request has been approved. The pet owner will contact you soon.',
        'notification_type': 'request_update'
    },
    {
        'title': 'New Pet Reported in Your Area',
        'message': 'A new pet has been reported found near your location. Check it out!',
        'notification_type': 'new_pet_report'
    },
    {
        'title': 'Welcome to PetRescue!',
        'message': 'Thank you for joining our community. Together we can help reunite pets with their families.',
        'notification_type': 'system_message'
    }
]

for i, notif_data in enumerate(notification_data):
    user = created_users[i % len(created_users)]
    
    notification, created = Notification.objects.get_or_create(
        recipient=user,
        title=notif_data['title'],
        defaults={
            'message': notif_data['message'],
            'notification_type': notif_data['notification_type'],
            'is_read': random.choice([True, False])
        }
    )
    if created:
        print(f"Created notification for {user.username}: {notification.title}")

print(f"\nSample data creation completed!")
print(f"Created {len(created_users)} users")
print(f"Created {len(created_pets)} pets")
print(f"Created {PetRequest.objects.count()} pet requests")
print(f"Created {Notification.objects.count()} notifications")
print("\nYou can now log in with any of the created users using password: 'password123'")
print("Admin user credentials: username='admin', password='admin123'")