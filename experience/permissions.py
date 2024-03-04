from rest_framework.permissions import BasePermission
from .serializers import ExperienceSerializer
from user_id_from_token import get_user_id_from_request, extract_jwt_token


class IsExperienceOwner(BasePermission):
    def has_object_permission(self, request, view, experience):
        # Get the id of the authenticated user
        user_id = get_user_id_from_request(request)

        if request.method == 'GET':
            return True

        if request.method == 'POST':
            if str(user_id) == request.data['employee_id']:
                return True

        if request.method == 'PUT':
            experience_data = ExperienceSerializer(experience).data
            # Check if the employee_id matches between the request, logged in user and object
            if experience_data['employee_id'] == user_id == int(request.data['employee_id']):
                return True
            return False
        if request.method == 'DELETE':
            experience_data = ExperienceSerializer(experience).data
            if int(experience_data['employee_id']) == user_id:
                return True
            return False

        return False
