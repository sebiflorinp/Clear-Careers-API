from rest_framework.permissions import BasePermission
from .serializers import EmployeeSerializer, EmployerSerializer
from user_id_from_token import get_user_id_from_request


class IsEmployeeAccountOwner(BasePermission):
    def has_object_permission(self, request, view, employee):
        if request.method == 'GET' or request.method == 'POST':
            return True

        if request.method == 'PUT':
            user_id = get_user_id_from_request(request)
            employee_data = EmployeeSerializer(employee).data
            # Check if user_id matches with employee_id from object and request
            if request.data['employee_id'] == employee_data['employee_id'] == user_id:
                return True
            return False


class IsEmployerAccountOwner(BasePermission):
    def has_object_permission(self, request, view, employer):
        if request.method == 'GET' or request.method == 'POST':
            return True

        if request.method == 'PUT':
            user_id = get_user_id_from_request(request)
            employer_data = EmployerSerializer(employer).data
            # Check if user_id matches with employer_id from the request and object
            if request.data['employer_id'] == employer_data['employer_id'] == user_id:
                return True
            return False
