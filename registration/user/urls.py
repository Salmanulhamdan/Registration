from django.urls import path
from .views import AdminDashboardView, EditorDashboardView, RegistrationView,LoginView, StaffDashboardView, StudentDashboardView
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('student/dashboard/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('staff/dashboard/', StaffDashboardView.as_view(), name='staff_dashboard'),
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('editor/dashboard/', EditorDashboardView.as_view(), name='editor_dashboard'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]

