from django import forms
from captcha.fields import ReCaptchaField


class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, required=False)
    email = forms.EmailField(label='Email Address', max_length=200, required=True)
    subject = forms.CharField(label='Message Purpose', required=True)
    message = forms.CharField(label='Message', widget=forms.Textarea, max_length=2000, required=True)
    cc_myself = forms.BooleanField(required=False)


class ListingForm(forms.Form):
    email = forms.EmailField(label='Email Address', max_length=200, required=False)
    message = forms.CharField(label='Message', max_length=400, required=True, widget=forms.Textarea)
    captcha = ReCaptchaField(label='Captcha')
