from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from posting.serializers import PostingSerializer
from authentication.models import User, Employer
from posting.models import Posting


class TestPostingsEndpoint(APITestCase):
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

        self.valid_posting_data = {
            'employer_id': self.employer1.employer_id.id,
            'job_title': 'Frontend Developer'
        }

        self.invalid_posting_data = {
            'employer_id': self.employer1.employer_id.id,
        }

        self.get_url = reverse('list-postings')
        self.post_url = reverse('create-postings', kwargs={'employer_id': self.employer1.employer_id.id})
        self.put_url = reverse('update-delete-postings', kwargs={'employer_id': self.employer1.employer_id.id,
                                                                 'posting_id': self.posting1.posting_id})
        self.delete_url = reverse('update-delete-postings', kwargs={'employer_id': self.employer1.employer_id.id,
                                                                    'posting_id': self.posting1.posting_id})

    def test_list_all_postings(self):
        response = self.client.get(self.get_url)
        postings = Posting.objects.all()
        serializer = PostingSerializer(postings, many=True)

        self.assertEqual(serializer.data, response.data)

    def test_creating_posting_with_valid_data(self):
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.post_url, self.valid_posting_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creating_posting_with_invalid_data(self):
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.post_url, self.invalid_posting_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creating_posting_without_authentication(self):
        response = self.client.post(self.post_url, self.invalid_posting_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creating_posting_with_the_wrong_authentication(self):
        token = AccessToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.post_url, self.valid_posting_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_updating_posting_with_valid_data(self):
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.put_url, self.valid_posting_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_updating_posting_with_invalid_data(self):
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.put_url, self.invalid_posting_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_updating_posting_that_does_not_exist(self):
        url = reverse('update-delete-postings', kwargs={'employer_id': self.employer1.employer_id.id,
                                                        'posting_id': 500})
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(url, self.valid_posting_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_updating_posting_without_authorization(self):
        response = self.client.put(self.put_url, self.valid_posting_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_updating_posting_with_the_wrong_authentication(self):
        token = AccessToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.put_url, self.valid_posting_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deleting_existent_posting(self):
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_deleting_non_existent_posting(self):
        url = reverse('update-delete-postings', kwargs={'employer_id': self.employer1.employer_id.id,
                                                        'posting_id': 500})
        token = AccessToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deleting_posting_without_authentication(self):
        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_deleting_posting_with_the_wrong_authentication(self):
        token = AccessToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)








