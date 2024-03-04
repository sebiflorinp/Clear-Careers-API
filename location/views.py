from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsLocationOwner
from authentication.models import Employer
from .models import Location
from rest_framework.response import Response
from rest_framework import status
from .serializers import LocationSerializer


class CreateLocations(APIView):
    serializer_class = LocationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsLocationOwner]

    def post(self, request, *args, **kwargs):
        try:
            employer_id = kwargs.get('employer_id')
            # Check if employer_id is valid
            Employer.objects.get(employer_id=employer_id)
            # Check if there are any other hqs, the first location must be the hq and there cannot be more than one hq
            hqs = Location.objects.filter(employer_id=employer_id, is_hq=True)
            if (request.data['is_hq'].lower() == 'true' and len(hqs) != 0 or request.data['is_hq'].lower() == 'false'
                    and len(hqs) == 0):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # Check if the employer_id from the request matches with the one from the endpoint
            if employer_id != int(request.data['employer_id']):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # Create the object
            location = LocationSerializer(data=request.data)
            # Check permissions
            self.check_object_permissions(request, location)
            if location.is_valid():
                location.save()
                return Response(location.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Employer.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateDeleteLocations(APIView):
    serializer_class = LocationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsLocationOwner]

    def put(self, request, *args, **kwargs):
        try:
            employer_id = kwargs.get('employer_id')
            # Check if the location exists
            location = (Location.objects
                        .filter(employer_id=employer_id)
                        .get(location_id=kwargs.get('location_id'))
                        )
            # Check if the id of the request matches with the id form the endpoint
            if kwargs.get('location_id') != int(request.data['location_id']):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # Check permissions
            self.check_object_permissions(request, location)
            # Update the location
            updated_location = LocationSerializer(location, data=request.data)
            if updated_location.is_valid():
                updated_location.save()
                return Response(updated_location.data)
            else:
                return Response(updated_location.errors, status=status.HTTP_400_BAD_REQUEST)
        except Location.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            # Check if the location exists
            location = (Location.objects
                        .filter(employer_id=kwargs.get('employer_id'))
                        .get(location_id=kwargs.get('location_id'))
                        )
            # Check permissions
            self.check_object_permissions(request, location)
            # Delete the location
            location.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Location.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
