from rest_framework.permissions import BasePermission
from user_id_from_token import get_user_id_from_request
from .serializers import LocationSerializer


class IsLocationOwner(BasePermission):
    def has_object_permission(self, request, view, location):
        user_id = get_user_id_from_request(request)

        if request.method == 'POST':
            # Check if the employer_id from the request matches with the user_id
            if int(request.data['employer_id']) == user_id:
                return True
            return False

        if request.method == 'PUT':
            location_data = LocationSerializer(location).data
            # Check if the user_id matches with the employer_id from the request and location object
            if user_id == int(request.data['employer_id']) == location_data['employer_id']:
                return True
            return False

        if request.method == 'DELETE':
            location_data = LocationSerializer(location).data
            # Check if the user_id matches with the employer_id from the location object
            if user_id == location_data['employer_id']:
                return True
            return False
