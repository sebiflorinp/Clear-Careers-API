from django.urls import path, include
from .views import RetrieveUpdateEmployees, CreateListEmployees, CreateListEmployers, RetrieveUpdateEmployers

djoser_patterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt'))
]

employee_patterns = [
    path('employees/<int:employee_id>', RetrieveUpdateEmployees.as_view(),
         name='retrieve-update-delete-employees'),
    path('employees/', CreateListEmployees.as_view(), name='create-list-employees')
]

employer_patterns = [
    path('employers/', CreateListEmployers.as_view(), name='create-list-employers'),
    path('employers/<int:employer_id>', RetrieveUpdateEmployers.as_view(),
         name='retrieve-update-employers')
]

urlpatterns = djoser_patterns + employee_patterns + employer_patterns
