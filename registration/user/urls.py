from django.urls import path
from .views import RegistrationView

urlpatterns = [
    path('', RegistrationView.as_view(), name='registration'),
    # path('login/', LoginView.as_view(), name='login'),

]