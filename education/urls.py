from django.urls import path
from .views import CreateEducation, UpdateDeleteEducation

urlpatterns = [
    path('employee/<int:employee_id>/education/', CreateEducation.as_view(), name='create-education'),
    path('employee/<int:employee_id>/education/<int:education_id>', UpdateDeleteEducation.as_view(),
         name='update-delete-education')
]