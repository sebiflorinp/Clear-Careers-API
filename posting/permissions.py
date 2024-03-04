from rest_framework.permissions import BasePermission
from user_id_from_token import get_user_id_from_request
from posting.serializers import PostingSerializer


class IsPostingOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_id = get_user_id_from_request(request)

        if request.method == 'GET':
            return True

        if request.method == 'POST':
            # Check if the user_id from the token matches the employer_id from the request
            if user_id == int(request.data['employer_id']):
                return True
            return False

        if request.method == 'PUT':
            posting_data = PostingSerializer(obj).data
            # Check if the user_id from the token matches with the employer_id from the object and request
            if user_id == posting_data['employer_id'] == int(request.data['employer_id']):
                return True
            return False

        if request.method == 'DELETE':
            posting_data = PostingSerializer(obj).data
            # Check if the user_id from the token matches with the employer_id from the object
            if user_id == posting_data['employer_id']:
                return True
            return False
