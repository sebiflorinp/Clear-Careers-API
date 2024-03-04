from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from authentication.models import User
from notification.models import Notification
from notification.permissions import IsNotificationReceiver
from notification.serializers import NotificationSerializer


class CreateListNotifications(APIView):
    serializer_class = NotificationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsNotificationReceiver]

    def get(self, request, *args, **kwargs):
        # Check if the user exists
        try:
            receiver_id = kwargs.get('receiver_id')
            user = User.objects.get(id=receiver_id)
            # Get all notifications
            notifications = Notification.objects.filter(receiver_id=receiver_id)
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        # Check if the receiver_id matches with the one from the endpoint
        if int(request.data['receiver_id']) != kwargs.get('receiver_id'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # Create the notification
        notification = NotificationSerializer(data=request.data)
        # Check permissions
        self.check_object_permissions(request, notification)
        if notification.is_valid():
            notification.save()
            return Response(notification.data)
        else:
            return Response(notification.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteNotifications(APIView):
    serializer_class = NotificationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsNotificationReceiver]

    def delete(self, request, *args, **kwargs):
        # Check if the notification exists
        try:
            notification = (Notification.objects.filter(receiver_id=kwargs.get('receiver_id'))
                                                .get(notification_id=kwargs.get('notification_id')))
            # Check permissions
            self.check_object_permissions(request, notification)
            # Delete notification
            notification.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Notification.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

