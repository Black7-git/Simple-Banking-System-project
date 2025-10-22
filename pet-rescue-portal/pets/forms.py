"""
Forms for PetRescue application
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Pet, Request, Comment, UserProfile


class UserRegistrationForm(UserCreationForm):
    """Form for user registration"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile"""
    class Meta:
        model = UserProfile
        fields = ['phone', 'address']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PetReportForm(forms.ModelForm):
    """Form for reporting a found or lost pet"""
    class Meta:
        model = Pet
        fields = [
            'name', 'pet_type', 'breed', 'color', 'size', 'age_approximate',
            'distinctive_marks', 'status', 'location_found', 'date_found',
            'contact_phone', 'contact_email', 'photo', 'additional_info'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pet name (if known)'}),
            'pet_type': forms.Select(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Breed (if known)'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primary color'}),
            'size': forms.Select(attrs={'class': 'form-control'}),
            'age_approximate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2 years, puppy, adult'}),
            'distinctive_marks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Collar, tags, scars, unique markings, etc.'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'location_found': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street, area, city'}),
            'date_found': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your contact number'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email address'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'additional_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Any other helpful information'}),
        }


class PetSearchForm(forms.Form):
    """Form for searching pets"""
    search_query = forms.CharField(
        max_length=200, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, breed, color, or location...'
        })
    )
    pet_type = forms.ChoiceField(
        choices=[('', 'All Types')] + list(Pet.PET_TYPE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + list(Pet.PET_STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    size = forms.ChoiceField(
        choices=[('', 'All Sizes')] + list(Pet.PET_SIZE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class RequestForm(forms.ModelForm):
    """Form for creating a request"""
    class Meta:
        model = Request
        fields = ['request_type', 'pet', 'subject', 'description']
        widgets = {
            'request_type': forms.Select(attrs={'class': 'form-control'}),
            'pet': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief summary of your request'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Detailed description of your request'}),
        }


class AdminRequestUpdateForm(forms.ModelForm):
    """Form for admin to update request status"""
    class Meta:
        model = Request
        fields = ['status', 'admin_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'admin_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Admin notes and response'}),
        }


class CommentForm(forms.ModelForm):
    """Form for adding comments to pet reports"""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add a comment or provide additional information...'
            })
        }
