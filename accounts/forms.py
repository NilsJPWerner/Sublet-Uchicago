from django import forms
from .models import ExtendedUser

from allauth.account.forms import UserForm, PasswordField, SetPasswordField
from allauth.account import app_settings
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from allauth.account.utils import filter_users_by_email


class ExtendedUserForm(forms.ModelForm):
    class Meta:
        model = ExtendedUser
        fields = ('first_name', 'last_name', 'profile_picture', 'phone_number', 'uni_division', 'home_town', 'description',)
        widgets = {
          "profile_picture": forms.FileInput(attrs={'style': 'display: none;'}),
          "uni_division": forms.Select(attrs={'class': 'ui dropdown'}),
        }


# Subclassed to get rid of placeholder data
class ChangePasswordFormModified(UserForm):

    oldpassword = PasswordField(label=(""))
    password1 = SetPasswordField(label=(""))
    password2 = PasswordField(label=(""))

    def clean_oldpassword(self):
        if not self.user.check_password(self.cleaned_data.get("oldpassword")):
            raise forms.ValidationError(("Please type your current"
                                          " password."))
        return self.cleaned_data["oldpassword"]

    def clean_password2(self):
        if ("password1" in self.cleaned_data and "password2" in self.cleaned_data):
            if (self.cleaned_data["password1"] != self.cleaned_data["password2"]):
                raise forms.ValidationError(("You must type the same password"
                                              " each time."))
        return self.cleaned_data["password2"]

    def save(self):
        get_adapter().set_password(self.user, self.cleaned_data["password1"])


class AddEmailFormCombined(UserForm):

    add_email = forms.EmailField(label=("E-mail"),
                                 required=True,
                                 widget=forms.TextInput(attrs={"type": "email",
                                                                "size": "30"}))

    def clean_email(self):
        value = self.cleaned_data["add_email"]
        value = get_adapter().clean_email(value)
        errors = {
            "this_account": ("This e-mail address is already associated"
                              " with this account."),
            "different_account": ("This e-mail address is already associated"
                                   " with another account."),
        }
        users = filter_users_by_email(value)
        on_this_account = [u for u in users if u.pk == self.user.pk]
        on_diff_account = [u for u in users if u.pk != self.user.pk]

        if on_this_account:
            raise forms.ValidationError(errors["this_account"])
        if on_diff_account and app_settings.UNIQUE_EMAIL:
            raise forms.ValidationError(errors["different_account"])
        return value

    def save(self, request):
        return EmailAddress.objects.add_email(request,
                                              self.user,
                                              self.cleaned_data["add_email"],
                                              confirm=True)