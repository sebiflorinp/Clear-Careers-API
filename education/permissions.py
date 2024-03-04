from rest_framework.permissions import BasePermission
from .serializers import EducationSerializer
from user_id_from_token import get_user_id_from_request


class IsEducationOwner(BasePermission):
    def has_object_permission(self, request, view, education):
        user_id = get_user_id_from_request(request)

        if request.method == 'GET':
            return True

        if request.method == 'POST':
            # Check if the employee_id from the request matches with the user_id from the token
            if int(request.data['employee_id']) == user_id:
                return True
            return False

        if request.method == 'PUT':
            education_data = EducationSerializer(education).data
            # Check if the employee_id matches between the education object, request and user_id from the token
            if education_data['employee_id'] == user_id == int(request.data['employee_id']):
                return True
            return False

        if request.method == 'DELETE':
            education_data = EducationSerializer(education).data
            # Check if the user_id of the token matches with the employee_id of the experience object
            if user_id == int(education_data['employee_id']):
                return True
            return False
