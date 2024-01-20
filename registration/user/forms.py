from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
import re
from django.contrib.auth import authenticate
class RegistrationForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'role', 'country', 'nationality', 'mobile', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        role = cleaned_data.get('role')
        country = cleaned_data.get('country')
        nationality = cleaned_data.get('nationality')
        mobile = cleaned_data.get('mobile')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # Additional server-side validation rules
        if not username:
            raise forms.ValidationError('Username is required.')

        if len(username) < 4:
            raise forms.ValidationError('Username must be at least 4 characters long.')

        if not email:
            raise forms.ValidationError('Email is required.')

        if not self.validate_email_format(email):
            raise forms.ValidationError('Invalid email format.')

        if not role:
            raise forms.ValidationError('Role is required.')

        if not country:
            raise forms.ValidationError('Country is required.')

        if not nationality:
            raise forms.ValidationError('Nationality is required.')

        if not mobile:
            raise forms.ValidationError('Mobile is required.')

        if not self.validate_mobile_number(mobile):
            raise forms.ValidationError('Invalid mobile number. Mobile number must start with 6, 7, 8, or 9 and have 10 digits.')

        if not password1:
            raise forms.ValidationError('Password is required.')

        if not self.validate_password(password1):
            raise forms.ValidationError('Invalid password. Password must be at least 8 characters and include at least one uppercase letter, one lowercase letter, and one digit.')

        if password1 != password2:
            raise forms.ValidationError('Passwords do not match.')

        return cleaned_data

    def validate_email_format(self, email):
        # Corrected email format validation logic
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        return re.match(email_pattern, email)

    def validate_mobile_number(self, mobile):
        # Custom mobile number validation logic
        mobile_pattern = r"^(?!([0-9])\1+$)[6789]\d{9}$"
        return re.match(mobile_pattern, mobile)

    def validate_password(self, password):
        # Custom password validation logic
        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
        return re.match(password_pattern, password)
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True  # Activate the user upon registration

        # Set is_staff based on the role
        if user.role != 'student':
            user.is_staff = True
        else:
            user.is_staff = False

        # Set is_superuser for the admin role
        if user.role == 'admin':
            user.is_superuser = True
        else:
            user.is_superuser = False

        if commit:
            user.save()
        return user
    



class CustomLoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput(attrs={'autofocus': True}),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email.lower()  # Normalize email to lowercase

    def clean(self):
        super().clean()
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if not email:
            raise forms.ValidationError('Email cannot be empty.')

        if not password:
            raise forms.ValidationError('Password cannot be empty.')

     
        #  checking if it contains '@'
        if '@' not in email:
            raise forms.ValidationError('Please enter a valid email address.')

        # Authenticate the user
        user = authenticate(email=email, password=password)
        if user is None:
            raise forms.ValidationError('Invalid email or password.')

        if not user.is_active:
            raise forms.ValidationError('This account is inactive.')

        self.user_cache = user  # Save the authenticated user for later use

        return self.cleaned_data