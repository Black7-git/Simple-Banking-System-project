from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Pet, PetRequest, UserProfile


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            'name', 'pet_type', 'breed', 'color', 'gender', 'age', 'size',
            'location_found', 'description', 'finder_name', 'finder_phone',
            'finder_email', 'image'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'pet_type': forms.Select(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'size': forms.Select(attrs={'class': 'form-control'}),
            'location_found': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'finder_name': forms.TextInput(attrs={'class': 'form-control'}),
            'finder_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'finder_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class PetRequestForm(forms.ModelForm):
    class Meta:
        model = PetRequest
        fields = ['request_type', 'requester_name', 'requester_phone', 'requester_email', 'description', 'proof_of_ownership']
        widgets = {
            'request_type': forms.Select(attrs={'class': 'form-control'}),
            'requester_name': forms.TextInput(attrs={'class': 'form-control'}),
            'requester_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'requester_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'proof_of_ownership': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'is_volunteer', 'bio']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_volunteer': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class PetSearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, breed, color, or location...'
        })
    )
    pet_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Pet.PET_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    size = forms.ChoiceField(
        choices=[('', 'All Sizes')] + [('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )