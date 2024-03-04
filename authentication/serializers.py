from djoser.serializers import UserCreateSerializer
from .models import User, Employee, Employer
from rest_framework import serializers
from education.serializers import EducationSerializer
from experience.serializers import ExperienceSerializer
from location.serializers import LocationSerializer
from posting.serializers import PostingSerializer


class UserCredentialsSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['id', 'email', 'password', 'is_employee', 'is_employer']
        read_only_fields = ['id', 'email', 'password', 'is_employee', 'is_employer']


class EmployeeSerializer(serializers.ModelSerializer):
    user_credentials = UserCredentialsSerializer(read_only=True, source='employee_id')
    education = EducationSerializer(read_only=True, many=True)
    experience = ExperienceSerializer(read_only=True, many=True)

    class Meta:
        model = Employee
        fields = ['employee_id', 'user_credentials', 'phone_number', 'first_name', 'last_name', 'birthdate', 'country',
                  'city', 'description', 'education', 'experience']


class EmployerSerializer(serializers.ModelSerializer):
    user_credentials = UserCredentialsSerializer(read_only=True, source='employer_id')
    locations = LocationSerializer(read_only=True, many=True)
    postings = PostingSerializer(read_only=True, many=True)

    class Meta:
        model = Employer
        fields = ['employer_id', 'user_credentials', 'phone_number', 'website_link', 'company_name', 'industry',
                  'description', 'locations', 'postings']
