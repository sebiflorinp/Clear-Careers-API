from posting.models import Posting
from .models import Application
from .serializers import ApplicationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsApplicationOwnerOrReceiver
from authentication.models import User, Employer, Employee


class ListApplications(APIView):
    serializer_class = ApplicationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)


class CreateApplications(APIView):
    serializer_class = ApplicationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsApplicationOwnerOrReceiver]

    def post(self, request, *args, **kwargs):
        # Check if the employee exists
        employee_id = kwargs.get('employee_id')
        try:
            Employee.objects.get(employee_id=employee_id)
            # Check if the employee_id from the request matches with the one from the endpoint
            if employee_id != int(request.data['employee_id']):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            application = ApplicationSerializer(data=request.data)
            # Check if the posting exists
            try:
                posting = Posting.objects.get(posting_id=int(request.data['posting_id']))
            except Posting.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # Check if the posting is owned by the employer in the request
            if int(request.data['employer_id']) != posting.employer_id.employer_id.id:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # Check permissions
            self.check_object_permissions(request, application)
            # Create the application
            if application.is_valid():
                application.save()
                return Response(application.data)
            else:
                return Response(application.errors, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class DeleteApplications(APIView):
    serializer_class = ApplicationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsApplicationOwnerOrReceiver]

    def delete(self, request, *args, **kwargs):
        # Check if application exists
        try:
            application = Application.objects.get(application_id=kwargs.get('application_id'))
            # Check permissions
            self.check_object_permissions(request, application)
            application.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Application.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)