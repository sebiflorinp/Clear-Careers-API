from rest_framework.urls import path
from .views import ListApplications, CreateApplications, DeleteApplications

urlpatterns = [
    path('applications/', ListApplications.as_view(), name='list-applications'),
    path('employees/<int:employee_id>/applications/', CreateApplications.as_view(), name='create-applications'),
    path('aplications/<int:application_id>/', DeleteApplications.as_view(), name='delete-applications')
]