# users/views.py
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth import login # To log in the user immediately after registration

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home') # Redirect to home after successful registration
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        # Log the user in after successful registration
        login(self.request, self.object)
        return response

