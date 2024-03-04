from .models import Experience
from authentication.models import Employee
from .serializers import ExperienceSerializer
from rest_framework.views import APIView
from .permissions import IsExperienceOwner
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class CreateExperience(APIView):
    serializer_class = ExperienceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsExperienceOwner]

    def post(self, request, *args, **kwargs):
        # Check if the employee exists
        try:
            employee_id = kwargs.get('employee_id')
            employee = Employee.objects.get(employee_id=employee_id)
            # Check if the employee_id matches with the one from the request
            if str(employee_id) != request.data['employee_id']:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # Create the object
            experience = ExperienceSerializer(data=request.data)
            self.check_object_permissions(request, experience)
            if experience.is_valid():
                # Check permissions
                experience.save()
                return Response(experience.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateDeleteExperience(APIView):
    serializer_class = ExperienceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsExperienceOwner]

    def put(self, request, *args, **kwargs):
        # Check if the experience from the endpoint exists
        try:
            # Get experience
            experience = (Experience.objects
                          .filter(employee_id=kwargs.get('employee_id'))
                          .get(experience_id=kwargs.get('experience_id'))
                          )
            # Check if the experience_id from the endpoint matches with the one in the request.
            if request.data['experience_id'] != str(kwargs.get('experience_id')):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # Check permissions
            self.check_object_permissions(request, experience)
            # Perform the update
            updated_experience = ExperienceSerializer(experience, data=request.data)
            if updated_experience.is_valid():
                updated_experience.save()
                return Response(updated_experience.data)
            else:
                return Response(updated_experience.errors, status=status.HTTP_400_BAD_REQUEST)
        except Experience.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        # Check if the experience endpoint exists
        try:
            experience = (Experience.objects
                          .filter(employee_id=kwargs.get('employee_id'))
                          .get(experience_id=kwargs.get('experience_id'))
                          )
            # Check permissions
            self.check_object_permissions(request, experience)
            # Perform the deletion
            experience.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Experience.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
