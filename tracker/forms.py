from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Profile


class RegisterForm(forms.Form):
    """Form for new registration fields"""

    username = forms.CharField(
        label = "Username",
        max_length = 150,
        required = True,
        widget = forms.TextInput(attrs = {
            "class": "form-control",
            "id": "username",
            "placeholder": "Username",
        }),
    )
    display_name = forms.CharField(
        label = "Display Name (Optional)",
        max_length = 150,
        required = False, 
        widget = forms.TextInput(attrs = {
            "class": "form-control",
            "id": "display-name",
            "placeholder": "Display Name (Optional)",
        }),
    )
    password = forms.CharField(
        label = "Enter Password",
        max_length = 150,
        required = True,
        widget = forms.PasswordInput(attrs = {
            "class":"form-control",
            "id": "password",
            "placeholder":"Enter Password",
        }),
    )
    confirm_password = forms.CharField(
        label = "Confirm Password",
        max_length = 150,
        required=True,
        widget = forms.PasswordInput(attrs = {
            "class":"form-control",
            "id": "confirm-password",
            "placeholder":"Confirm Password",
        }),
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Validate - User has entered username and password
        if (not username) or (not password) or (not confirm_password):
            raise ValidationError("Must enter username and password.")

        # Validate - Username should be unique
        usernames = User.objects.values_list('username', flat=True)
        if username and username in usernames:
            raise ValidationError("Username already taken.")

        # Validate - Both passwords should match
        if (password and confirm_password) and password != confirm_password:
                raise ValidationError("Passwords must match.")
        

class ProfileForm(forms.ModelForm):
    """Form to edit user profile"""

    class Meta:
        model = Profile
        fields = ["display_name", "avatar"]
        labels = {
            "display_name": "Change Display Name",
        }
        widgets = {
            "display_name": forms.TextInput(attrs = {
                "class": "form-control",
                "placeholder": "Change Display Name",      
            })
        }