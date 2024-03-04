from django.urls import path
from .views import ListPostings, CreatePostings, UpdateDeletePostings

urlpatterns = [
    path('postings/', ListPostings.as_view(), name='list-postings'),
    path('employers/<int:employer_id>/postings/', CreatePostings.as_view(), name='create-postings'),
    path('employers/<int:employer_id>/postings/<int:posting_id>', UpdateDeletePostings.as_view(),
         name='update-delete-postings')
]