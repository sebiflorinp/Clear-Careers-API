from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from application.models import Application
from application.serializers import ApplicationSerializer
from authentication.models import User, Employee, Employer
from posting.models import Posting


class TestApplicationsEndpoints(APITestCase):
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

        self.user3 = User.objects.create(
            email="ionescuuul@gmail.com",
            password="qwerty",
            is_employer=True
        )

        self.employer1 = Employer.objects.create(
            employer_id=self.user3,
            phone_number='074568913',
            company_name='Amazon',
            industry='Tech',
            description='A nice company',
        )

        self.user4 = User.objects.create(
            email="georgescuuuul@gmail.com",
            password="qwerty",
            is_employer=True
        )

        self.employer2 = Employer.objects.create(
            employer_id=self.user4,
            phone_number='074568913',
            company_name='BitDefender',
            industry='Tech',
            description='Another nice company'
        )

        self.posting1 = Posting.objects.create(
            employer_id=self.employer1,
            job_title='Backend developer',
            location='Bucuresti',
            job_description='A nice job.',
            qualifications='Knows how to use Spring Boot',
            benefits='Meal tickets',
            employment_type='Full time',
            employment_arrangement='On-site'
        )

        self.application = Application.objects.create(
            employer_id=self.employer1,
            employee_id=self.employee2,
            posting_id=self.posting1
        )

        self.valid_application_data = {
            'employee_id': self.employee1.employee_id.id,
            'employer_id': self.employer1.employer_id.id,
            'posting_id': self.posting1.posting_id
        }
        self.post_url = reverse('create-applications', kwargs={'employee_id': self.employee1.employee_id.id})
        self.get_url = reverse('list-applications')
        self.delete_url = reverse('delete-applications', kwargs={'application_id': self.application.application_id})

    def test_getting_all_applications(self):
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        response = self.client.get(self.get_url)

        self.assertEqual(response.data, serializer.data)

    def test_getting_all_applications_without_authentication(self):
        response = self.client.get(self.get_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creating_application_with_valid_data(self):
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.post_url, self.valid_application_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creating_application_with_employer_that_does_not_exist(self):
        self.valid_application_data['employer_id'] = 5000
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.post_url, self.valid_application_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creating_application_with_employee_that_does_not_exist(self):
        self.valid_application_data['employee_id'] = 5000
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.post_url, self.valid_application_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creating_application_with_posting_that_does_not_exist(self):
        self.valid_application_data['posting_id'] = 5000
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.post_url, self.valid_application_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creating_application_with_employer_who_is_not_the_owner_of_the_posting(self):
        self.valid_application_data['employer_id'] = self.employer2.employer_id.id
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.post_url, self.valid_application_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creating_application_with_two_employees_in_the_request(self):
        self.valid_application_data['employer_id'] = self.employee2.employee_id.id
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.post_url, self.valid_application_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creating_application_without_authentication(self):
        response = self.client.post(self.post_url, self.valid_application_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creating_application_with_the_wrong_authentication(self):
        token = AccessToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.post_url, self.valid_application_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deleting_application_as_employee(self):
        token = AccessToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_deleting_application_as_employer(self):
        token = AccessToken.for_user(self.user3)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_deleting_application_that_does_not_exist(self):
        url = reverse('delete-applications', kwargs={'application_id': 5000})
        token = AccessToken.for_user(self.user3)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deleting_application_without_authentication(self):
        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_deleting_application_with_wrong_authentication(self):
        token = AccessToken.for_user(self.user4)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)







