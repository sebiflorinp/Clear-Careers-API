from .models import Education
from authentication.models import Employee
from .serializers import EducationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsEducationOwner


class CreateEducation(APIView):
    serializer_class = EducationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEducationOwner]

    def post(self, request, *args, **kwargs):
        # Check if the employer_id is valid
        try:
            employee_id = kwargs.get('employee_id')
            employee = Employee.objects.get(employee_id=employee_id)
            # Check if the employee_id matches between the request and endpoint
            if request.data['employee_id'] != str(employee_id):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # Create the instance
            education = EducationSerializer(data=request.data)
            if education.is_valid():
                # Check permissions
                self.check_object_permissions(request, education)
                education.save()
                return Response(education.data)
            else:
                return Response(education.errors, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateDeleteEducation(APIView):
    serializer_class = EducationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEducationOwner, IsAuthenticated]

    def put(self, request, *args, **kwargs):
        # Check if the education with the input id exists
        try:
            # Get the education that will be updated
            education = (Education.objects
                         .filter(employee_id=kwargs.get('employee_id'))
                         .get(education_id=kwargs.get('education_id'))
                         )
            # Check permissions
            self.check_object_permissions(request, education)
            # Perform the update
            updated_education = EducationSerializer(education, data=request.data)
            if updated_education.is_valid():
                updated_education.save()
                return Response(updated_education.data)
            else:
                return Response(updated_education.errors, status=status.HTTP_400_BAD_REQUEST)
        except Education.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        # Check if the education with the input id exists
        try:
            # Get the education that will be deleted
            education = (Education.objects
                         .filter(employee_id=kwargs.get('employee_id'))
                         .get(education_id=kwargs.get('education_id')))
            # Check permissions
            self.check_object_permissions(request, education)
            # delete the education
            education.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Education.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
