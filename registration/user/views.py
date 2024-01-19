from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from .forms import RegistrationForm
from .models import UserProfile

# Create your views here.

class RegistrationView(View):
    template_name = 'registration.html'


    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Check user's role and set privileges accordingly
            if user.role == 'admin':
                UserProfile.objects.create_superuser(
                    email=user.email,
                    password=user.password,
                    role=user.role,
                    username=user.username,
                    country=user.country,
                    nationality=user.nationality,
                    mobile=user.mobile,
                    is_active=user.is_active
                )
            elif user.role != 'student':
                user.is_staff = True
                user.save()

            # Log in the user after registration
            login(request, user)

            # Redirect to the login page
            return redirect('login')
        return render(request, self.template_name, {'form': form})