from django import forms
from .models import listing, ExtendedUser

class ListingForm(forms.ModelForm):
  class Meta: 
    model = listing
    fields = ['description', 'price', 'location' , 'details']


class ExtendedUserForm(forms.ModelForm):
    class Meta:
        model = ExtendedUser
        fields = ('first_name', 'last_name', 'profile_picture', 'phone_number', 'uni_division', 'description')
        widgets = {
          "profile_picture": forms.FileInput(attrs={'class': 'ui'}),
          "uni_division": forms.Select(attrs={'class': 'ui dropdown'}),
        }