from django import forms
from .models import Listing


class EditDescriptionForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('name', 'summary', 'price')


class EditLocationForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('street_address', 'apt', 'city', 'state', 'zip_code', 'latitude', 'longitude')


class EditDetailsForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('bed_size', 'roommate_count', 'bathroom', 'ac', 'in_unit_washer_dryer', 'tv',
            'cable_tv', 'internet', 'wheel_chair_accessible', 'pets_live_here', 'pets_allowed')
        widgets = {
            'bed_size': forms.Select(attrs={'class': 'ui dropdown'}),
            'bathroom': forms.Select(attrs={'class': 'ui dropdown'}),
            'roommate_count': forms.Select(attrs={'class': 'ui dropdown'}),
        }


class EditCalendarForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('fall_quarter', 'winter_quarter', 'spring_quarter', 'summer_quarter', 'start_date', 'end_date')
