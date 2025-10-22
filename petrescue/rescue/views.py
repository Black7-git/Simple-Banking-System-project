from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import Pet, PetRequest, Notification, UserProfile
from .forms import PetForm, PetRequestForm, UserRegistrationForm, UserProfileForm
from django.contrib.auth.models import User


def home(request):
    """Home page showing recent found pets"""
    recent_pets = Pet.objects.filter(status='found', is_verified=True).order_by('-date_found')[:6]
    stats = {
        'total_found': Pet.objects.filter(status='found').count(),
        'total_reunited': Pet.objects.filter(status='reunited').count(),
        'total_adopted': Pet.objects.filter(status='adopted').count(),
        'pending_requests': PetRequest.objects.filter(status='pending').count(),
    }
    return render(request, 'rescue/home.html', {
        'recent_pets': recent_pets,
        'stats': stats
    })


def pet_list(request):
    """List all found pets with search and filter functionality"""
    pets = Pet.objects.filter(status='found', is_verified=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        pets = pets.filter(
            Q(name__icontains=search_query) |
            Q(breed__icontains=search_query) |
            Q(color__icontains=search_query) |
            Q(location_found__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by pet type
    pet_type = request.GET.get('pet_type', '')
    if pet_type:
        pets = pets.filter(pet_type=pet_type)
    
    # Filter by size
    size = request.GET.get('size', '')
    if size:
        pets = pets.filter(size=size)
    
    # Pagination
    paginator = Paginator(pets, 12)
    page_number = request.GET.get('page')
    pets = paginator.get_page(page_number)
    
    return render(request, 'rescue/pet_list.html', {
        'pets': pets,
        'search_query': search_query,
        'pet_type': pet_type,
        'size': size,
    })


def pet_detail(request, pet_id):
    """Detail view for a specific pet"""
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'rescue/pet_detail.html', {'pet': pet})


def report_pet(request):
    """Form to report a found pet"""
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            if request.user.is_authenticated:
                pet.created_by = request.user
            else:
                # Create a temporary user for anonymous submissions
                pet.created_by = User.objects.get_or_create(username='anonymous')[0]
            pet.save()
            messages.success(request, 'Pet report submitted successfully! We will review it soon.')
            return redirect('pet_detail', pet_id=pet.id)
    else:
        form = PetForm()
    
    return render(request, 'rescue/report_pet.html', {'form': form})


def request_pet(request, pet_id):
    """Form to request a pet (claim or adopt)"""
    pet = get_object_or_404(Pet, id=pet_id)
    
    if request.method == 'POST':
        form = PetRequestForm(request.POST)
        if form.is_valid():
            request_obj = form.save(commit=False)
            request_obj.pet = pet
            request_obj.save()
            
            # Create notification for admin
            Notification.objects.create(
                user=pet.created_by,
                notification_type='pet_found',
                title=f'New {request_obj.request_type} request',
                message=f'{request_obj.requester_name} has submitted a {request_obj.request_type} request for {pet}.',
                related_pet=pet,
                related_request=request_obj
            )
            
            messages.success(request, 'Your request has been submitted successfully!')
            return redirect('pet_detail', pet_id=pet.id)
    else:
        form = PetRequestForm()
    
    return render(request, 'rescue/request_pet.html', {
        'form': form,
        'pet': pet
    })


def search_lost_pet(request):
    """Search for lost pets"""
    if request.method == 'POST':
        search_query = request.POST.get('search_query', '')
        pets = Pet.objects.filter(
            Q(name__icontains=search_query) |
            Q(breed__icontains=search_query) |
            Q(color__icontains=search_query) |
            Q(description__icontains=search_query),
            status='found',
            is_verified=True
        )
        return render(request, 'rescue/search_results.html', {
            'pets': pets,
            'search_query': search_query
        })
    
    return render(request, 'rescue/search_lost_pet.html')


def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'rescue/register.html', {'form': form})


@login_required
def profile(request):
    """User profile page"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    # Get user's pets and requests
    user_pets = Pet.objects.filter(created_by=request.user)
    user_requests = PetRequest.objects.filter(requester_email=request.user.email)
    
    return render(request, 'rescue/profile.html', {
        'form': form,
        'user_pets': user_pets,
        'user_requests': user_requests
    })


@login_required
def notifications(request):
    """User notifications"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Mark all as read
    notifications.update(is_read=True)
    
    return render(request, 'rescue/notifications.html', {
        'notifications': notifications
    })


# Admin views
@login_required
def admin_dashboard(request):
    """Admin dashboard"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    stats = {
        'total_pets': Pet.objects.count(),
        'pending_verification': Pet.objects.filter(is_verified=False).count(),
        'pending_requests': PetRequest.objects.filter(status='pending').count(),
        'recent_pets': Pet.objects.order_by('-date_found')[:5],
        'recent_requests': PetRequest.objects.order_by('-created_at')[:5],
    }
    
    return render(request, 'rescue/admin_dashboard.html', {'stats': stats})


@login_required
def manage_requests(request):
    """Admin view to manage pet requests"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    requests = PetRequest.objects.all().order_by('-created_at')
    return render(request, 'rescue/manage_requests.html', {'requests': requests})


@login_required
def approve_request(request, request_id):
    """Approve a pet request"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    pet_request = get_object_or_404(PetRequest, id=request_id)
    pet_request.status = 'approved'
    pet_request.processed_by = request.user
    pet_request.save()
    
    # Update pet status
    if pet_request.request_type == 'claim':
        pet_request.pet.status = 'reunited'
    elif pet_request.request_type == 'adopt':
        pet_request.pet.status = 'adopted'
    pet_request.pet.save()
    
    # Create notification
    Notification.objects.create(
        user=pet_request.pet.created_by,
        notification_type='request_approved',
        title='Request Approved',
        message=f'Your {pet_request.request_type} request for {pet_request.pet} has been approved.',
        related_pet=pet_request.pet,
        related_request=pet_request
    )
    
    messages.success(request, 'Request approved successfully!')
    return redirect('manage_requests')


@login_required
def reject_request(request, request_id):
    """Reject a pet request"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    pet_request = get_object_or_404(PetRequest, id=request_id)
    pet_request.status = 'rejected'
    pet_request.processed_by = request.user
    pet_request.save()
    
    # Create notification
    Notification.objects.create(
        user=pet_request.pet.created_by,
        notification_type='request_rejected',
        title='Request Rejected',
        message=f'Your {pet_request.request_type} request for {pet_request.pet} has been rejected.',
        related_pet=pet_request.pet,
        related_request=pet_request
    )
    
    messages.success(request, 'Request rejected.')
    return redirect('manage_requests')