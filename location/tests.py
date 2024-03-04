from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from authentication.models import User, Employer
from location.models import Location


class TestLocationsEndpoint(APITestCase):
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

        self.location1 = Location.objects.create(
            employer_id=self.employer1,
            country='Romania',
            city='Cluj',
            street='Avram Iancu',
            street_number='5',
            is_hq=True
        )

        self.user2 = User.objects.create(
            email="georgescu@gmail.com",
            password="qwerty",
            is_employer=True
        )

        self.employer2 = Employer.objects.create(
            employer_id=self.user2,
            phone_number='074568913',
            company_name='BitDefender',
            industry='Tech',
            description='Another nice company'
        )

        self.valid_location_hq_data = {
            'employer_id': self.employer2.employer_id.id,
            'country': 'Romania',
            'city': 'Bucuresti',
            'street': 'Victoriei',
            'street_number': 2,
            'is_hq': 'True'
        }

        self.valid_location_non_hq_data = {
            'employer_id': self.employer1.employer_id.id,
            'country': 'Romania',
            'city': 'Bucuresti',
            'street': 'Victoriei',
            'street_number': 2,
            'is_hq': 'False'
        }

        self.invalid_location_non_hq_data = {
            'employer_id': self.employer1.employer_id.id,
            'street_number': 2,
            'is_hq': 'False'
        }
        self.post_url_employer_1 = reverse('create-locations',
                                           kwargs={'employer_id': self.employer1.employer_id.id})
        self.post_url_employer_2 = reverse('create-locations',
                                           kwargs={'employer_id': self.employer2.employer_id.id})
        self.put_url = reverse('update-delete-locations', kwargs={'employer_id': self.employer1.employer_id.id,
                                                                  'location_id': self.location1.location_id})
        self.delete_url = reverse('update-delete-locations',
                                  kwargs={'employer_id': self.employer1.employer_id.id,
                                          'location_id': self.location1.location_id})

    def test_creating_a_location_with_valid_data(self):
        token = AccessToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.post_url_employer_2, self.valid_location_hq_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creating_a_non_hq_location_when_there_are_no_hqs(self):
        token = AccessToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.post_url_employer_2, self.valid_location_non_hq_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creating_a_hq_location_when_the_same_employer_already_has_a_hq(self):
        self.valid_location_hq_data['employer_id'] = self.employer1.employer_id.id
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.post_url_employer_1, self.valid_location_hq_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creating_a_location_with_invalid_data(self):
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.post_url_employer_1, self.invalid_location_non_hq_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creating_a_location_without_authentication(self):
        response = self.client.post(self.post_url_employer_1, self.invalid_location_non_hq_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creating_a_location_with_the_wrong_authentication(self):
        token = AccessToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.post_url_employer_1, self.valid_location_non_hq_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_updating_a_location_with_valid_data(self):
        self.valid_location_non_hq_data['location_id'] = self.location1.location_id
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.put_url, self.valid_location_non_hq_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_updating_a_location_with_invalid_data(self):
        self.invalid_location_non_hq_data['location_id'] = self.location1.location_id
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.put_url, self.invalid_location_non_hq_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_updating_a_location_without_authentication(self):
        self.valid_location_non_hq_data['location_id'] = self.location1.location_id
        response = self.client.put(self.put_url, self.valid_location_non_hq_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_updating_a_location_with_wrong_authentication(self):
        self.valid_location_non_hq_data['location_id'] = self.location1.location_id
        token = AccessToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.put_url, self.valid_location_non_hq_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_updating_a_location_that_does_not_exist(self):
        url = reverse('update-delete-locations', kwargs={'employer_id': self.employer1.employer_id.id,
                                                                  'location_id': 500})
        self.valid_location_non_hq_data['location_id'] = 500
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.put_url, self.valid_location_non_hq_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deleting_a_location_that_exists(self):
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_deleting_a_location_that_does_not_exist(self):
        url = reverse('update-delete-locations', kwargs={'employer_id': self.employer1.employer_id.id,
                                                         'location_id': 500})
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deleting_a_location_without_authentication(self):
        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_deleting_a_location_with_the_wrong_authentication(self):
        token = AccessToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
