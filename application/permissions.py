from rest_framework.permissions import BasePermission
from user_id_from_token import get_user_id_from_request
from .serializers import ApplicationSerializer


class IsApplicationOwnerOrReceiver(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_id = get_user_id_from_request(request)

        if request.method == 'POST':
            # Check if the user_id from the token matches with the employer_id from the request
            if user_id == int(request.data['employee_id']):
                return True
            return False

        if request.method == 'DELETE':
            # Check if the user_id from the token matches with the employer_id from the object
            application_data = ApplicationSerializer(obj).data
            if user_id == int(application_data['employer_id']) or user_id == int(application_data['employee_id']):
                return True
            return False
