from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from .forms import RegistrationForm,CustomLoginForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import  login
from django.contrib import messages

# Create your views here.

class RegistrationView(View):
    template_name = 'registration.html'


    def get(self, request):
        # Check if the user is already authenticated
        if request.user.is_authenticated:
            # Determine the user's role
            role = request.user.role 

            # Redirect based on the user's role
            if role == 'student':
                return redirect('student_dashboard')
            elif role == 'staff':
                return redirect('staff_dashboard')
            elif role == 'admin':
                return redirect('admin_dashboard')
            elif role == 'editor':
                return redirect('editor_dashboard')
            
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
        return render(request, self.template_name, {'form': form})
    



def is_student(user):
    return user.role == 'student'

def is_staff(user):
    return user.role == 'staff'

def is_admin(user):
    return user.role == 'admin'

def is_editor(user):
    return user.role == 'editor'



class LoginView(View):
    template_name = 'login.html'
    form_class = CustomLoginForm

    def get(self, request, *args, **kwargs):
        # Check if the user is already authenticated
        if request.user.is_authenticated:
            # Determine the user's role
            role = request.user.role 

            # Redirect based on the user's role
            if role == 'student':
                return redirect('student_dashboard')
            elif role == 'staff':
                return redirect('staff_dashboard')
            elif role == 'admin':
                return redirect('admin_dashboard')
            elif role == 'editor':
                return redirect('editor_dashboard')
            
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.user_cache  # Access the authenticated user directly from the form
            login(request, user)
            
            role = user.role

            if role == 'student':
                return redirect('student_dashboard')
            elif role == 'staff':
                return redirect('staff_dashboard')
            elif role == 'admin':
                return redirect('admin_dashboard')
            elif role == 'editor':
                return redirect('editor_dashboard')
        else:
            messages.error(request, 'Invalid login credentials.')

        return render(request, self.template_name, {'form': form})
    




class StudentDashboardView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'
    template_name = 'student_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not is_student(request.user):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class StaffDashboardView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'
    template_name = 'staff_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not is_staff(request.user):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class AdminDashboardView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'
    template_name = 'admin_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not is_admin(request.user):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class EditorDashboardView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'
    template_name = 'editor_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not is_editor(request.user):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
            

     