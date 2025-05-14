from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name') # Role will be set in the view

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.ROLE_STUDENT # Default role for new sign-ups
        # You might want to add email uniqueness check here if not handled by model's unique=True
        if commit:
            user.save()
        return user