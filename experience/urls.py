from django.urls import path
from .views import CreateExperience, UpdateDeleteExperience

urlpatterns = [
    path('employees/<int:employee_id>/experiences/', CreateExperience.as_view(), name='create-experience'),
    path('employees/<int:employee_id>/experiences/<int:experience_id>', UpdateDeleteExperience.as_view(),
         name='update-delete-experience')
]