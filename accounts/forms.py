from django import forms
from .models import listing

class ListingForm(forms.ModelForm):
	class Meta: 
		model = listing
		fields = ['description', 'price', 'location' , 'details']