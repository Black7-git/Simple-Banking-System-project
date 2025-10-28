from django import forms
from .models import Pet, PetImage, PetRequest

class PetReportForm(forms.ModelForm):
    """Form for reporting found or lost pets"""
    
    class Meta:
        model = Pet
        fields = [
            'name', 'pet_type', 'breed', 'color', 'size', 'age_estimate', 'gender',
            'description', 'distinctive_features', 'status', 'found_location', 
            'found_date', 'current_location', 'contact_phone', 'contact_email'
        ]
        widgets = {
            'found_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'distinctive_features': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes for styling
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] = 'form-control'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'
        
        # Add placeholders
        self.fields['name'].widget.attrs['placeholder'] = 'Pet\'s name (if known)'
        self.fields['breed'].widget.attrs['placeholder'] = 'e.g., Golden Retriever, Persian Cat'
        self.fields['color'].widget.attrs['placeholder'] = 'e.g., Brown and white, Black'
        self.fields['age_estimate'].widget.attrs['placeholder'] = 'e.g., Young, 2-3 years, Senior'
        self.fields['found_location'].widget.attrs['placeholder'] = 'Street address or general area'
        self.fields['current_location'].widget.attrs['placeholder'] = 'Where is the pet now?'

class PetImageForm(forms.ModelForm):
    """Form for uploading pet images"""
    
    class Meta:
        model = PetImage
        fields = ['image', 'caption']
        widgets = {
            'caption': forms.TextInput(attrs={'placeholder': 'Optional caption for the image'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['caption'].widget.attrs['class'] = 'form-control'

class PetSearchForm(forms.Form):
    """Form for searching pets"""
    query = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, breed, color, or location...'
        })
    )
    pet_type = forms.ChoiceField(
        choices=[('', 'All Types')] + list(Pet.PET_TYPES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + list(Pet.STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    size = forms.ChoiceField(
        choices=[('', 'All Sizes')] + list(Pet.PET_SIZES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class PetRequestForm(forms.ModelForm):
    """Form for creating pet requests"""
    
    class Meta:
        model = PetRequest
        fields = ['request_type', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['request_type'].widget.attrs['class'] = 'form-select'
        self.fields['message'].widget.attrs['class'] = 'form-control'
        self.fields['message'].widget.attrs['placeholder'] = 'Please provide additional details about your request...'