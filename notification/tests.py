from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from authentication.models import User, Employer, Employee
from notification.models import Notification
from notification.serializers import NotificationSerializer


class TestNotificationEndpoints(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            email="ionescu@gmail.com",
            password="qwerty",
            is_employer=True
        )

        self.employer1 = Employer.objects.create(
            employer_id=self.user1,
            phone_number='074568913',
            company_name='Amazon',
            industry='Tech',
            description='A nice company',
        )

        self.user2 = User.objects.create(
            email='tudorescu@gmail.com',
            password='qwerty',
            is_employee=True
        )

        self.employee2 = Employee.objects.create(
            employee_id=self.user2,
            phone_number='07123456',
            first_name='George',
            last_name='Tudorescu',
            birthdate='2000-01-21',
            country='Romania',
            city='Iasi',
            description='A construction worker.'
        )

        self.notification = Notification.objects.create(
            receiver_id=self.user1,
            description='An important notification',
        )

        self.valid_notification_data = {
            'receiver_id': self.user1.id,
            'description': 'Another important notification',
        }

        self.invalid_notification_data = {
            'receiver_id': self.user1.id
        }

        self.list_post_url = reverse('create-list-notifications', kwargs={'receiver_id': self.user1.id})
        self.delete_url = reverse('delete-notifications', kwargs={'receiver_id': self.user1.id,
                                                                  'notification_id': self.notification.notification_id})

    def test_getting_all_notifications(self):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.list_post_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_getting_all_notification_without_authentication(self):
        response = self.client.get(self.list_post_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creating_notification_with_valid_data(self):
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.list_post_url, self.valid_notification_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creating_notification_with_invalid_data(self):
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.list_post_url, self.invalid_notification_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creating_notification_without_authentication(self):
        response = self.client.post(self.list_post_url, self.invalid_notification_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creating_notification_with_the_wrong_authentication(self):
        token = AccessToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.list_post_url, self.valid_notification_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deleting_an_existent_notification(self):
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_deleting_a_non_existent_notification(self):
        url = reverse('delete-notifications', kwargs={'receiver_id': self.user1.id,
                                                      'notification_id': 5000})
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deleting_notification_without_authentication(self):
        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_deleting_notification_with_the_wrong_authentication(self):
        token = AccessToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)




