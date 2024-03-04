from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from authentication.models import User, Employee
from experience.models import Experience


class TestExperienceEndpoints(APITestCase):
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

        self.experience1 = Experience.objects.create(
            employee_id=self.employee1,
            employer_name='Bitdefender',
            title='Cyber Security expert',
            description='Ensuring the security of an enterprise application.',
            start_year=2000,
            end_year=2003
        )

        self.experience2 = Experience.objects.create(
            employee_id=self.employee1,
            employer_name='Accenture',
            title='Cyber Security expert',
            description='Ensuring the security of an enterprise application.',
            start_year=2003,
            end_year=2006
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

        self.valid_experience_data = {
            'employee_id': self.employee1.employee_id_id,
            'employer_name': 'Amazon',
            'title': 'Backend developer',
            'description': 'Had to create Flask APIs',
            'start_year': 2001,
            'end_year': 2004
        }

        self.invalid_experience_data = {
            'employee_id': self.employee1.employee_id.id,
            'employer_name': 'Amazon',
            'end_year': 2004
        }

        self.post_url = reverse('create-experience', kwargs={'employee_id': self.employee1.employee_id_id})
        self.put_url = reverse('update-delete-experience', kwargs={'employee_id': self.employee1.employee_id_id,
                                                                   'experience_id': self.experience1.experience_id})
        self.delete_url = reverse('update-delete-experience',
                                  kwargs={'employee_id': self.employee1.employee_id.id,
                                          'experience_id': self.experience1.experience_id})

    def test_creating_experience_with_valid_data(self):
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.post_url, self.valid_experience_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creating_experience_with_invalid_data(self):
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.post_url, self.invalid_experience_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creating_experience_without_authentication(self):
        response = self.client.post(self.post_url, self.valid_experience_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creating_experience_with_wrong_authentication(self):
        token = AccessToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.post_url, self.valid_experience_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_updating_experience_with_valid_data(self):
        self.valid_experience_data['experience_id'] = self.experience1.experience_id
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.put_url, self.valid_experience_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_updating_experience_with_invalid_data(self):
        self.invalid_experience_data['experience_id'] = self.experience1.experience_id
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.put_url, self.invalid_experience_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_updating_experience_without_authentication(self):
        self.valid_experience_data['experience_id'] = self.experience1.experience_id
        response = self.client.put(self.put_url, self.valid_experience_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_updating_experience_wit_wrong_authentication(self):
        self.valid_experience_data['experience_id'] = self.experience1.experience_id
        token = AccessToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.put_url, self.valid_experience_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_updating_experience_with_wrong_experience_id(self):
        self.valid_experience_data['experience_id'] = self.experience2.experience_id
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.put_url, self.valid_experience_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_updating_non_existent_experience(self):
        url = reverse('update-delete-experience', kwargs={'employee_id': self.employee1.employee_id.id,
                                                          'experience_id': 5000})
        self.valid_experience_data['experience_id'] = 5000
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.put_url, self.valid_experience_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deleting_existent_experience(self):
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_deleting_non_existent_experience(self):
        url = reverse('update-delete-experience', kwargs={'employee_id': self.employee1.employee_id.id,
                                                          'experience_id': 5000})
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
