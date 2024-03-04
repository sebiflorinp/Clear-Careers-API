from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, is_employer, is_employee, password=None):

        if not email:
            return ValueError('Email is a required value.')
        if not password:
            return ValueError('password is a required value.')
        if not is_employee and not is_employer:
            return ValueError('the user needs to be an employee or an employer')
        if is_employer == is_employee:
            return ValueError('the user cannot be an employer and an employee at the same time.')

        email = self.normalize_email(email)
        user = self.model(email=email, is_employee=is_employee, is_employer=is_employer)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=200, unique=True, blank=False, null=False)
    is_employer = models.BooleanField(default=False, blank=False, null=False)
    is_employee = models.BooleanField(default=False, blank=False, null=False)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['is_employer', 'is_employee', 'password']

    objects = UserManager()

    def __str__(self):
        return self.email


class Employee(models.Model):
    employee_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    birthdate = models.DateField(null=False, blank=False)
    country = models.CharField(max_length=30, null=False, blank=False)
    city = models.CharField(max_length=30, null=False, blank=False)
    description = models.CharField(max_length=1000, null=False, blank=False)

    @property
    def education(self):
        return self.education_set.all()

    @property
    def experience(self):
        return self.experience_set.all()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Employer(models.Model):
    employer_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    website_link = models.CharField(max_length=100, null=False, blank=True, default="")
    company_name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    industry = models.CharField(max_length=30, null=False, blank=False)
    description = models.CharField(max_length=1000, null=False, blank=False)

    @property
    def locations(self):
        return self.location_set.all()

    @property
    def postings(self):
        return self.posting_set.all()

    def __str__(self):
        return f"{self.company_name}"
