from django.urls import path
from .views import CreateLocations, UpdateDeleteLocations

urlpatterns = [
    path('employers/<int:employer_id>/locations/', CreateLocations.as_view(), name='create-locations'),
    path('employers/<int:employer_id>/locations/<int:location_id>', UpdateDeleteLocations.as_view(),
         name='update-delete-locations')
]