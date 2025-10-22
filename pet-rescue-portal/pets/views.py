"""
Views for PetRescue application
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Pet, Request, Notification, Comment, UserProfile
from .forms import (
    UserRegistrationForm, PetReportForm, PetSearchForm, 
    RequestForm, CommentForm, AdminRequestUpdateForm, UserProfileForm
)


def home(request):
    """Home page view"""
    # Get recent pets
    recent_lost_pets = Pet.objects.filter(status='LOST').order_by('-created_at')[:6]
    recent_found_pets = Pet.objects.filter(status='FOUND').order_by('-created_at')[:6]
    
    # Statistics
    total_pets = Pet.objects.count()
    lost_pets = Pet.objects.filter(status='LOST').count()
    found_pets = Pet.objects.filter(status='FOUND').count()
    reunited_pets = Pet.objects.filter(status='REUNITED').count()
    
    context = {
        'recent_lost_pets': recent_lost_pets,
        'recent_found_pets': recent_found_pets,
        'total_pets': total_pets,
        'lost_pets': lost_pets,
        'found_pets': found_pets,
        'reunited_pets': reunited_pets,
    }
    return render(request, 'pets/home.html', context)


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(
                user=user,
                phone=form.cleaned_data.get('phone', ''),
                address=form.cleaned_data.get('address', '')
            )
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to PetRescue.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'pets/register.html', {'form': form})


def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'pets/login.html')


def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile(request):
    """User profile view"""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=user_profile)
    
    # Get user's pets and requests
    user_pets = Pet.objects.filter(reported_by=request.user)
    user_requests = Request.objects.filter(requester=request.user)
    
    context = {
        'profile_form': profile_form,
        'user_pets': user_pets,
        'user_requests': user_requests,
    }
    return render(request, 'pets/profile.html', context)


@login_required
def report_pet(request):
    """Report a found or lost pet"""
    if request.method == 'POST':
        form = PetReportForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.reported_by = request.user
            pet.save()
            messages.success(request, 'Pet report submitted successfully!')
            return redirect('pet_detail', pk=pet.pk)
    else:
        form = PetReportForm()
    
    return render(request, 'pets/report_pet.html', {'form': form})


def pet_list(request):
    """List all pets with search and filtering"""
    pets = Pet.objects.all()
    form = PetSearchForm(request.GET)
    
    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        pet_type = form.cleaned_data.get('pet_type')
        status = form.cleaned_data.get('status')
        size = form.cleaned_data.get('size')
        
        if search_query:
            pets = pets.filter(
                Q(name__icontains=search_query) |
                Q(breed__icontains=search_query) |
                Q(color__icontains=search_query) |
                Q(location_found__icontains=search_query)
            )
        
        if pet_type:
            pets = pets.filter(pet_type=pet_type)
        
        if status:
            pets = pets.filter(status=status)
        
        if size:
            pets = pets.filter(size=size)
    
    # Pagination
    paginator = Paginator(pets, 12)  # 12 pets per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'pets': page_obj,
    }
    return render(request, 'pets/pet_list.html', context)


def pet_detail(request, pk):
    """View details of a specific pet"""
    pet = get_object_or_404(Pet, pk=pk)
    comments = pet.comments.all()
    
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.pet = pet
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('pet_detail', pk=pk)
    else:
        comment_form = CommentForm()
    
    context = {
        'pet': pet,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'pets/pet_detail.html', context)


@login_required
def edit_pet(request, pk):
    """Edit pet information"""
    pet = get_object_or_404(Pet, pk=pk)
    
    # Check if user is owner or admin
    if pet.reported_by != request.user and not request.user.profile.is_admin:
        messages.error(request, 'You do not have permission to edit this pet.')
        return redirect('pet_detail', pk=pk)
    
    if request.method == 'POST':
        form = PetReportForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pet information updated successfully!')
            return redirect('pet_detail', pk=pk)
    else:
        form = PetReportForm(instance=pet)
    
    return render(request, 'pets/edit_pet.html', {'form': form, 'pet': pet})


@login_required
def delete_pet(request, pk):
    """Delete a pet report"""
    pet = get_object_or_404(Pet, pk=pk)
    
    # Check if user is owner or admin
    if pet.reported_by != request.user and not request.user.profile.is_admin:
        messages.error(request, 'You do not have permission to delete this pet.')
        return redirect('pet_detail', pk=pk)
    
    if request.method == 'POST':
        pet.delete()
        messages.success(request, 'Pet report deleted successfully!')
        return redirect('pet_list')
    
    return render(request, 'pets/delete_pet.html', {'pet': pet})


@login_required
def create_request(request):
    """Create a new request"""
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.requester = request.user
            req.save()
            messages.success(request, 'Request submitted successfully!')
            return redirect('request_detail', pk=req.pk)
    else:
        form = RequestForm()
        # Filter pets to only show user's pets or all pets based on request type
        form.fields['pet'].queryset = Pet.objects.all()
    
    return render(request, 'pets/create_request.html', {'form': form})


@login_required
def request_list(request):
    """List all requests"""
    if request.user.profile.is_admin:
        requests = Request.objects.all()
    else:
        requests = Request.objects.filter(requester=request.user)
    
    # Pagination
    paginator = Paginator(requests, 10)  # 10 requests per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'requests': page_obj,
    }
    return render(request, 'pets/request_list.html', context)


@login_required
def request_detail(request, pk):
    """View details of a specific request"""
    req = get_object_or_404(Request, pk=pk)
    
    # Check permissions
    if req.requester != request.user and not request.user.profile.is_admin:
        messages.error(request, 'You do not have permission to view this request.')
        return redirect('request_list')
    
    context = {
        'request': req,
    }
    return render(request, 'pets/request_detail.html', context)


@login_required
def admin_panel(request):
    """Admin panel view"""
    if not request.user.profile.is_admin:
        messages.error(request, 'You do not have admin privileges.')
        return redirect('home')
    
    # Statistics
    total_users = UserProfile.objects.count()
    total_pets = Pet.objects.count()
    pending_requests = Request.objects.filter(status='PENDING').count()
    unverified_pets = Pet.objects.filter(is_verified=False).count()
    
    # Recent data
    recent_requests = Request.objects.filter(status='PENDING')[:10]
    recent_pets = Pet.objects.filter(is_verified=False)[:10]
    
    context = {
        'total_users': total_users,
        'total_pets': total_pets,
        'pending_requests': pending_requests,
        'unverified_pets': unverified_pets,
        'recent_requests': recent_requests,
        'recent_pets': recent_pets,
    }
    return render(request, 'pets/admin_panel.html', context)


@login_required
def admin_update_request(request, pk):
    """Admin view to update request status"""
    if not request.user.profile.is_admin:
        messages.error(request, 'You do not have admin privileges.')
        return redirect('home')
    
    req = get_object_or_404(Request, pk=pk)
    
    if request.method == 'POST':
        form = AdminRequestUpdateForm(request.POST, instance=req)
        if form.is_valid():
            req = form.save(commit=False)
            req.resolved_by = request.user
            if req.status in ['RESOLVED', 'REJECTED']:
                req.resolved_at = timezone.now()
            req.save()
            
            # Create notification for requester
            Notification.objects.create(
                user=req.requester,
                notification_type='REQUEST_UPDATE',
                title=f'Request Update: {req.subject}',
                message=f'Your request has been updated to {req.get_status_display()}.',
                related_request=req
            )
            
            messages.success(request, 'Request updated successfully!')
            return redirect('admin_panel')
    else:
        form = AdminRequestUpdateForm(instance=req)
    
    return render(request, 'pets/admin_update_request.html', {'form': form, 'request': req})


@login_required
def admin_verify_pet(request, pk):
    """Admin view to verify a pet report"""
    if not request.user.profile.is_admin:
        messages.error(request, 'You do not have admin privileges.')
        return redirect('home')
    
    pet = get_object_or_404(Pet, pk=pk)
    pet.is_verified = True
    pet.verified_by = request.user
    pet.save()
    
    # Create notification for reporter
    Notification.objects.create(
        user=pet.reported_by,
        notification_type='SYSTEM',
        title='Pet Report Verified',
        message=f'Your pet report for {pet.name or "the pet"} has been verified.',
        related_pet=pet
    )
    
    messages.success(request, 'Pet report verified successfully!')
    return redirect('admin_panel')


@login_required
def notifications(request):
    """View user notifications"""
    user_notifications = request.user.notifications.all()
    
    # Mark all as read
    if request.method == 'POST':
        user_notifications.update(is_read=True)
        messages.success(request, 'All notifications marked as read.')
        return redirect('notifications')
    
    context = {
        'notifications': user_notifications,
    }
    return render(request, 'pets/notifications.html', context)


def about(request):
    """About page"""
    return render(request, 'pets/about.html')


def contact(request):
    """Contact page"""
    return render(request, 'pets/contact.html')
