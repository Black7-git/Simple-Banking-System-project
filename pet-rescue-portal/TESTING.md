# PetRescue Testing Guide

This document provides comprehensive testing procedures for the PetRescue application.

## Table of Contents
1. [Manual Testing](#manual-testing)
2. [Test Cases](#test-cases)
3. [User Acceptance Testing](#user-acceptance-testing)
4. [Admin Testing](#admin-testing)
5. [Security Testing](#security-testing)

## Manual Testing

### Prerequisites
- Application is installed and running
- Database is migrated
- At least one superuser account exists

## Test Cases

### 1. User Registration and Authentication

#### Test 1.1: User Registration
**Steps:**
1. Navigate to http://127.0.0.1:8000/register/
2. Fill in registration form:
   - Username: testuser1
   - First Name: Test
   - Last Name: User
   - Email: test@example.com
   - Phone: 555-0001
   - Address: 123 Test St
   - Password: TestPass123!
   - Confirm Password: TestPass123!
3. Submit form

**Expected Result:**
- User is created successfully
- Redirected to home page
- User is automatically logged in
- Success message displayed

#### Test 1.2: User Login
**Steps:**
1. Navigate to http://127.0.0.1:8000/login/
2. Enter credentials:
   - Username: testuser1
   - Password: TestPass123!
3. Submit form

**Expected Result:**
- User is logged in
- Redirected to home page
- Welcome message displayed
- User menu shows username

#### Test 1.3: Invalid Login
**Steps:**
1. Navigate to login page
2. Enter invalid credentials
3. Submit form

**Expected Result:**
- Login fails
- Error message displayed
- User remains on login page

#### Test 1.4: User Logout
**Steps:**
1. Click "Logout" in navigation
2. Confirm logout

**Expected Result:**
- User is logged out
- Redirected to home page
- Login/Register buttons appear
- Success message displayed

### 2. Pet Reporting

#### Test 2.1: Report Lost Pet
**Steps:**
1. Login as regular user
2. Click "Report Pet"
3. Fill in form:
   - Name: Max
   - Type: Dog
   - Breed: Golden Retriever
   - Color: Golden
   - Size: Large
   - Status: Lost
   - Location: Central Park
   - Date: Today's date
   - Contact Phone: 555-0001
   - Contact Email: test@example.com
   - Distinctive Marks: White spot on chest
   - Upload photo (optional)
4. Submit form

**Expected Result:**
- Pet report created
- Redirected to pet detail page
- All information displays correctly
- Success message shown

#### Test 2.2: Report Found Pet
**Steps:**
1. Login as regular user
2. Report a found pet with status "Found"
3. Fill all required fields
4. Submit

**Expected Result:**
- Found pet report created
- Status shows "Found"
- Pet appears in search results

#### Test 2.3: Report Pet Without Photo
**Steps:**
1. Report a pet without uploading a photo
2. Submit form

**Expected Result:**
- Pet created successfully
- Default placeholder icon shown
- All other information displays correctly

### 3. Pet Search and Browse

#### Test 3.1: View All Pets
**Steps:**
1. Navigate to "Find Pets"
2. View list without filters

**Expected Result:**
- All pets displayed in grid
- Pagination works if more than 12 pets
- Pet cards show basic information

#### Test 3.2: Search by Text
**Steps:**
1. Go to "Find Pets"
2. Enter search term: "Max"
3. Click Search

**Expected Result:**
- Only pets matching "Max" in name, breed, color, or location shown
- Search maintains filters

#### Test 3.3: Filter by Type
**Steps:**
1. Go to "Find Pets"
2. Select "Dog" from Pet Type dropdown
3. Click Search

**Expected Result:**
- Only dogs displayed
- Other types filtered out

#### Test 3.4: Filter by Status
**Steps:**
1. Select "Lost" from Status dropdown
2. Click Search

**Expected Result:**
- Only lost pets shown
- Found/Reunited pets filtered out

#### Test 3.5: Combined Filters
**Steps:**
1. Use multiple filters:
   - Search: "Golden"
   - Type: Dog
   - Status: Lost
   - Size: Large
2. Click Search

**Expected Result:**
- Only pets matching ALL criteria shown
- Filters work in combination

### 4. Pet Details and Interaction

#### Test 4.1: View Pet Details
**Steps:**
1. Click on any pet card
2. View detail page

**Expected Result:**
- All pet information displayed
- Contact information visible
- Photo displayed (or placeholder)
- Comments section shown

#### Test 4.2: Add Comment
**Steps:**
1. View pet detail page (logged in)
2. Scroll to comments section
3. Enter comment: "I saw this pet yesterday near Main St"
4. Click "Post Comment"

**Expected Result:**
- Comment posted successfully
- Comment appears in list
- Username and timestamp shown

#### Test 4.3: Edit Own Pet
**Steps:**
1. View detail page of pet you reported
2. Click "Edit"
3. Modify information (e.g., change status to "Reunited")
4. Submit

**Expected Result:**
- Pet updated successfully
- Changes reflected on detail page
- Success message shown

#### Test 4.4: Delete Own Pet
**Steps:**
1. View detail of pet you reported
2. Click "Delete"
3. Confirm deletion

**Expected Result:**
- Confirmation page shown
- After confirmation, pet deleted
- Redirected to pet list

### 5. Request Management

#### Test 5.1: Create Request
**Steps:**
1. Login as user
2. Click "My Requests"
3. Click "Create New Request"
4. Fill form:
   - Type: I Lost My Pet
   - Subject: Request help finding my dog
   - Description: My dog Max went missing...
5. Submit

**Expected Result:**
- Request created
- Status is "Pending"
- Appears in "My Requests"

#### Test 5.2: View Request Details
**Steps:**
1. Go to "My Requests"
2. Click on a request

**Expected Result:**
- Full request details shown
- Status clearly displayed
- Admin notes shown if available

### 6. User Profile

#### Test 6.1: View Profile
**Steps:**
1. Login
2. Click username in navigation
3. View profile page

**Expected Result:**
- User information displayed
- List of user's pets shown
- List of user's requests shown

#### Test 6.2: Update Profile
**Steps:**
1. View profile page
2. Update phone number and address
3. Click "Update Profile"

**Expected Result:**
- Profile updated successfully
- New information displayed
- Success message shown

### 7. Admin Functions

#### Test 7.1: Access Admin Panel
**Steps:**
1. Login as admin user
2. Click "Admin Panel"

**Expected Result:**
- Admin dashboard displayed
- Statistics shown correctly
- Pending requests listed
- Unverified pets listed

#### Test 7.2: Verify Pet Report
**Steps:**
1. Go to Admin Panel
2. Find unverified pet
3. Click "Verify"

**Expected Result:**
- Pet marked as verified
- Verification badge shown on pet detail
- Notification sent to reporter

#### Test 7.3: Update Request Status
**Steps:**
1. Go to Admin Panel
2. Click on pending request
3. Click "Update Request"
4. Change status to "In Progress"
5. Add admin notes
6. Submit

**Expected Result:**
- Request status updated
- Admin notes saved
- Notification sent to requester
- Timestamp recorded

#### Test 7.4: Resolve Request
**Steps:**
1. Update request status to "Resolved"
2. Add resolution notes
3. Submit

**Expected Result:**
- Request marked as resolved
- Resolved timestamp recorded
- Admin recorded as resolver
- Notification sent

### 8. Notifications

#### Test 8.1: View Notifications
**Steps:**
1. Login as user who has notifications
2. Click "Notifications"

**Expected Result:**
- All notifications listed
- Unread notifications highlighted
- Most recent first

#### Test 8.2: Mark All as Read
**Steps:**
1. View notifications page
2. Click "Mark All as Read"

**Expected Result:**
- All notifications marked as read
- Highlight removed
- Success message shown

### 9. Security Testing

#### Test 9.1: Protected Routes
**Steps:**
1. Logout
2. Try to access protected URLs directly:
   - /pets/report/
   - /profile/
   - /admin-panel/

**Expected Result:**
- Redirected to login page
- After login, redirected back to intended page

#### Test 9.2: Authorization Check
**Steps:**
1. Login as regular user (not admin)
2. Try to access /admin-panel/

**Expected Result:**
- Access denied
- Error message displayed
- Redirected to home page

#### Test 9.3: Edit Permission Check
**Steps:**
1. Login as User A
2. Try to edit pet reported by User B

**Expected Result:**
- Edit button not visible OR
- Access denied if URL accessed directly

### 10. Responsive Design

#### Test 10.1: Mobile View
**Steps:**
1. Open application on mobile device or resize browser to mobile width
2. Navigate through all pages

**Expected Result:**
- Navigation menu adapts to mobile
- Pet grid shows 1 column
- All features accessible
- No horizontal scrolling

#### Test 10.2: Tablet View
**Steps:**
1. Resize to tablet width (768px)
2. Navigate pages

**Expected Result:**
- Layout adjusts appropriately
- Pet grid shows 2 columns
- All content readable

### 11. File Upload

#### Test 11.1: Upload Valid Image
**Steps:**
1. Report pet with photo upload
2. Upload JPG, PNG, or GIF image

**Expected Result:**
- Image uploaded successfully
- Displays on pet detail page
- File saved to media/pet_photos/

#### Test 11.2: Large Image
**Steps:**
1. Try to upload very large image (>5MB)

**Expected Result:**
- Either uploads and is resized OR
- Shows appropriate error message

### 12. Error Handling

#### Test 12.1: 404 Page
**Steps:**
1. Navigate to non-existent URL

**Expected Result:**
- 404 error page displayed (or Django default if DEBUG=True)

#### Test 12.2: Form Validation
**Steps:**
1. Try to submit forms with missing required fields
2. Try invalid email formats
3. Try short passwords

**Expected Result:**
- Form validation errors shown
- User guided to correct errors
- Form data preserved

## User Acceptance Testing (UAT)

### Scenario 1: Lost Pet Owner
**User Story:** As a pet owner who lost my dog, I want to report it and search for matches.

**Steps:**
1. Register account
2. Report lost dog with details and photo
3. Search database for found dogs matching description
4. View potential matches
5. Comment on potential match
6. Create request for admin help

**Success Criteria:**
- All steps complete without errors
- Information accurately saved and displayed
- User can communicate with potential finders

### Scenario 2: Person Who Found Pet
**User Story:** As someone who found a pet, I want to report it so the owner can find it.

**Steps:**
1. Register account
2. Report found pet with description and photo
3. Verify contact information is displayed
4. Monitor comments for owner contact

**Success Criteria:**
- Found pet report created successfully
- Owner can find the pet through search
- Contact information accessible to searchers

### Scenario 3: Administrator
**User Story:** As an admin, I want to manage reports and help users.

**Steps:**
1. Login as admin
2. View pending requests
3. Verify pet reports
4. Update request statuses
5. Monitor platform activity

**Success Criteria:**
- Admin dashboard provides good overview
- Can efficiently process requests
- Users receive timely responses

## Performance Testing

### Test Database with Sample Data

Create test data:
```python
python manage.py shell

from django.contrib.auth.models import User
from pets.models import Pet, Request
import random
from datetime import datetime, timedelta

# Create test users
for i in range(20):
    User.objects.create_user(
        username=f'testuser{i}',
        email=f'test{i}@example.com',
        password='testpass123'
    )

# Create test pets
users = User.objects.all()
types = ['DOG', 'CAT', 'BIRD']
statuses = ['LOST', 'FOUND', 'REUNITED']

for i in range(100):
    Pet.objects.create(
        name=f'Pet{i}',
        pet_type=random.choice(types),
        color='Brown',
        status=random.choice(statuses),
        location_found=f'Location {i}',
        date_found=datetime.now().date() - timedelta(days=random.randint(1, 30)),
        reported_by=random.choice(users),
        contact_phone='555-0000',
        contact_email='test@example.com'
    )
```

Test pagination and search performance with 100+ records.

## Bug Reporting Template

When reporting bugs, include:

```
**Title:** Brief description

**Environment:**
- OS: 
- Browser:
- Django version:
- Database:

**Steps to Reproduce:**
1. 
2. 
3. 

**Expected Result:**

**Actual Result:**

**Screenshots:**

**Additional Notes:**
```

## Test Results Checklist

Use this checklist to track testing progress:

- [ ] User registration works
- [ ] User login/logout works
- [ ] Pet reporting (Lost) works
- [ ] Pet reporting (Found) works
- [ ] Pet search works
- [ ] Pet filters work
- [ ] Pet details display correctly
- [ ] Comments work
- [ ] Edit pet works
- [ ] Delete pet works
- [ ] Create request works
- [ ] View requests works
- [ ] Profile update works
- [ ] Admin panel accessible
- [ ] Pet verification works
- [ ] Request updates work
- [ ] Notifications work
- [ ] Security/permissions work
- [ ] Mobile responsive
- [ ] File upload works
- [ ] Error handling works

## Automated Testing (Future Enhancement)

To add automated tests, create `pets/tests.py`:

```python
from django.test import TestCase, Client
from django.contrib.auth.models import User
from pets.models import Pet, UserProfile

class PetRescueTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_user_registration(self):
        response = self.client.post('/register/', {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        })
        self.assertEqual(User.objects.count(), 2)
    
    # Add more tests...
```

Run with:
```bash
python manage.py test
```

## Conclusion

Complete all test cases before considering the application ready for deployment. Document any issues found and track their resolution.
