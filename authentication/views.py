from .models import Employer, Employee, User
from .serializers import EmployerSerializer, EmployeeSerializer, UserCredentialsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsEmployeeAccountOwner, IsEmployerAccountOwner
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny


class CreateListEmployees(APIView):
    serializer_class = EmployeeSerializer

    def get(self, request, *args, **kwargs):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.data['id'])
            # check if is_employee is True and is_employer False
            if not user.is_employee or user.is_employer:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user_data = UserCredentialsSerializer(user)
            # if there is already an employee or employer created with the received credentials return a 400
            employees = Employee.objects.filter(employee_id=request.data['id'])
            employers = Employer.objects.filter(employer_id=request.data['id'])
            if len(employees) > 0 or len(employers) > 0:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # Add the credentials and if to the received data
            request.data['employee_id'] = request.data['id']
            request.data['user'] = user_data.data
            employee = EmployeeSerializer(data=request.data)
            if employee.is_valid():
                employee.save()
                return Response(employee.data, status=status.HTTP_201_CREATED)
            else:
                return Response(employee.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RetrieveUpdateEmployees(APIView):
    serializer_class = EmployeeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeAccountOwner, IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            employee = Employee.objects.get(employee_id=kwargs.get('employee_id'))
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            # Get the employee to be updated
            employee = Employee.objects.get(employee_id=kwargs.get('employee_id'))
            # Check permissions
            self.check_object_permissions(request, employee)
            # Perform the update
            updated_employee = EmployeeSerializer(employee, data=request.data)
            if updated_employee.is_valid():
                updated_employee.save()
                return Response(updated_employee.data)
            else:
                return Response(updated_employee.errors, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateListEmployers(APIView):
    serializer_class = EmployerSerializer

    def get(self, request, *args, **kwargs):
        employers = Employer.objects.all()
        serializer = EmployerSerializer(employers, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.data['id'])
            # check if the credentials has is_employer is True and is_employee False
            if user.is_employee or not user.is_employer:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user_data = UserCredentialsSerializer(user)
            # check if the received credentials have an employee / employer account already associated with
            employees = Employee.objects.filter(employee_id=request.data['id'])
            employers = Employer.objects.filter(employer_id=request.data['id'])
            if len(employees) != 0 or len(employers) != 0:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # add the credentials and the employer_id to the received data
            request.data['user'] = user_data.data
            request.data['employer_id'] = request.data['id']
            employer = EmployerSerializer(data=request.data)
            if employer.is_valid():
                employer.save()
                return Response(employer.data)
            else:
                return Response(employer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RetrieveUpdateEmployers(APIView):
    serializer_class = EmployeeSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsEmployerAccountOwner, IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get(self, request, *args, **kwargs):
        try:
            employer = Employer.objects.get(employer_id=kwargs.get('employer_id'))
            serializer = EmployerSerializer(employer)
            return Response(serializer.data)
        except Employer.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            # Get employer to update
            employer = Employer.objects.get(employer_id=kwargs.get('employer_id'))
            # Check permissions
            self.check_object_permissions(request, employer)
            # Update the employer
            updated_employer = EmployerSerializer(employer, data=request.data)
            if updated_employer.is_valid():
                updated_employer.save()
                return Response(updated_employer.data)
            else:
                return Response(updated_employer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Employer.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
