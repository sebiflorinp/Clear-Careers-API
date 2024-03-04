from rest_framework.test import APITestCase
from .models import Education
from authentication.models import User
from .models import Employee
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status


class TestEducationEndpoints(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            email='ionescu@gmail.com',
            password='qwerty',
            is_employee=True
        )

        self.employee1 = Employee.objects.create(
            employee_id=self.user1,
            phone_number='07243456546',
            first_name='Vasile',
            last_name='Ionescu',
            birthdate='1990-3-12',
            country='Romania',
            city='Constanta',
            description='Nice guy'
        )

        self.education_employee1 = Education.objects.create(
            employee_id=self.employee1,
            institution_name='UBB',
            field='Computer Science',
            degree='Bachelors',
            start_year=2026,
            end_year=2029
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

        self.valid_education_data = {
            'employee_id': self.employee1.employee_id_id,
            'institution_name': 'UPB',
            'field': 'Math',
            'degree': 'Bachelors',
            'start_year': 2026,
            'end_year': 2029
        }

        self.invalid_education_data = {
            'employee_id': self.employee1.employee_id_id,
            'start_year': 2026,
            'end_year': 2029
        }
        self.post_url = reverse('create-education', kwargs={'employee_id': self.employee1.employee_id_id})
        self.put_url = reverse('update-delete-education', kwargs={'employee_id': self.employee1.employee_id_id,
                                                                  'education_id': self.education_employee1.education_id})
        self.delete_url = reverse('update-delete-education', kwargs={'employee_id': self.employee1.employee_id_id,
                                                                     'education_id': self.education_employee1.education_id})

    def test_create_education_with_valid_data(self):
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.post_url, self.valid_education_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_education_with_invalid_data(self):
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.post_url, self.invalid_education_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_education_without_authentication(self):
        response = self.client.post(self.post_url, self.valid_education_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_education_with_wrong_authentication(self):
        token = AccessToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.post_url, self.valid_education_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_with_valid_data(self):
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.put_url, self.valid_education_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_with_invalid_data(self):
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.put_url, self.invalid_education_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_education_that_does_not_exist(self):
        url = reverse('update-delete-education', kwargs={'employee_id': self.employee1.employee_id_id,
                                                                  'education_id': 5000})
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(url, self.valid_education_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_without_authentication(self):
        response = self.client.put(self.put_url, self.valid_education_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_with_wrong_authentication(self):
        token = AccessToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.put_url, self.valid_education_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deleting_existing_education(self):
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_deleting_non_existent_education(self):
        url = reverse('update-delete-education', kwargs={'employee_id': self.employee1.employee_id_id,
                                                         'education_id': 50000})
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deleting_without_authentication(self):
        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_deleting_with_wrong_authentication(self):
        token = AccessToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


