from rest_framework.permissions import BasePermission

from notification.serializers import NotificationSerializer
from user_id_from_token import get_user_id_from_request


class IsNotificationReceiver(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_id = get_user_id_from_request(request)

        if request.method == 'POST':
            if user_id == int(request.data['receiver_id']):
                return True
            return False

        if request.method == 'DELETE':
            notification_data = NotificationSerializer(obj).data
            if user_id == notification_data['receiver_id']:
                return True
            return False

