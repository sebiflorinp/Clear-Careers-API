from rest_framework.urls import path
from .views import CreateListNotifications, DeleteNotifications

urlpatterns = [
    path('users/<int:receiver_id>/notifications/', CreateListNotifications.as_view(), name='create-list-notifications'),
    path('users/<int:receiver_id>/notifications/<int:notification_id>/', DeleteNotifications.as_view(),
         name='delete-notifications')
]