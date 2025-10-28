from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Pet, PetImage, PetRequest
from .forms import PetReportForm, PetImageForm, PetSearchForm, PetRequestForm

def home_view(request):
    """Home page view"""
    recent_pets = Pet.objects.filter(is_verified=True).order_by('-created_at')[:6]
    search_form = PetSearchForm()
    
    context = {
        'recent_pets': recent_pets,
        'search_form': search_form,
    }
    return render(request, 'pets/home.html', context)

def pet_list_view(request):
    """View for listing all pets with search functionality"""
    form = PetSearchForm(request.GET)
    pets = Pet.objects.filter(is_verified=True)
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        pet_type = form.cleaned_data.get('pet_type')
        status = form.cleaned_data.get('status')
        size = form.cleaned_data.get('size')
        
        if query:
            pets = pets.filter(
                Q(name__icontains=query) |
                Q(breed__icontains=query) |
                Q(color__icontains=query) |
                Q(found_location__icontains=query) |
                Q(description__icontains=query)
            )
        
        if pet_type:
            pets = pets.filter(pet_type=pet_type)
        
        if status:
            pets = pets.filter(status=status)
        
        if size:
            pets = pets.filter(size=size)
    
    # Pagination
    paginator = Paginator(pets, 12)  # Show 12 pets per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'pets': page_obj,
    }
    return render(request, 'pets/pet_list.html', context)

def pet_detail_view(request, pet_id):
    """View for displaying pet details"""
    pet = get_object_or_404(Pet, id=pet_id, is_verified=True)
    
    # Handle pet request form submission
    if request.method == 'POST' and request.user.is_authenticated:
        request_form = PetRequestForm(request.POST)
        if request_form.is_valid():
            pet_request = request_form.save(commit=False)
            pet_request.pet = pet
            pet_request.requester = request.user
            pet_request.save()
            messages.success(request, 'Your request has been submitted successfully!')
            return redirect('pets:detail', pet_id=pet.id)
    else:
        request_form = PetRequestForm()
    
    context = {
        'pet': pet,
        'request_form': request_form,
    }
    return render(request, 'pets/pet_detail.html', context)

@login_required
def report_pet_view(request):
    """View for reporting found or lost pets"""
    if request.method == 'POST':
        pet_form = PetReportForm(request.POST)
        image_form = PetImageForm(request.POST, request.FILES)
        
        if pet_form.is_valid():
            pet = pet_form.save(commit=False)
            pet.reported_by = request.user
            pet.save()
            
            # Handle image upload
            if image_form.is_valid() and image_form.cleaned_data.get('image'):
                pet_image = image_form.save(commit=False)
                pet_image.pet = pet
                pet_image.save()
            
            messages.success(request, 'Pet report submitted successfully! It will be reviewed by our team.')
            return redirect('pets:detail', pet_id=pet.id)
    else:
        pet_form = PetReportForm()
        image_form = PetImageForm()
    
    context = {
        'pet_form': pet_form,
        'image_form': image_form,
    }
    return render(request, 'pets/report_pet.html', context)

@login_required
def my_reports_view(request):
    """View for displaying user's pet reports"""
    pets = Pet.objects.filter(reported_by=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(pets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'pets': page_obj,
    }
    return render(request, 'pets/my_reports.html', context)

@login_required
def my_requests_view(request):
    """View for displaying user's pet requests"""
    requests = PetRequest.objects.filter(requester=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(requests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'requests': page_obj,
    }
    return render(request, 'pets/my_requests.html', context)
