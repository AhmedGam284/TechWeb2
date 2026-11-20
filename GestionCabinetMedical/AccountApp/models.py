from datetime import timezone
from wsgiref.validate import validator
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator,MinLengthValidator,MaxLengthValidator

# Create your models here.
class User(AbstractUser):
    pass

number_validator = RegexValidator(r'^\d{8}$', 'Phone number must be 8 digits')

def birth_date_validator(date):
    if date >= timezone.localdate():
        raise ValidationError('Birth date must be in the past.')

#Doctor
class Doctor(User):
    license_number = models.CharField(max_length=6, unique=True , validators=[MinLengthValidator(6), MaxLengthValidator(6)])
    phone = models.CharField(max_length=8, unique=True,validators=[RegexValidator(regex=r'^\d{8}$', message='Phone number must be 8 digits')])
    specialities = models.ManytoManyField('Specialty', related_name='doctors')

#Patient
class Patient(User):
    national_id = models.CharField(max_length=8, unique=True , validators=[number_validator])
    phone = models.CharField(max_length=8, unique=True, validators=[number_validator])
    birth_date = models.DateField(validators=[birth_date_validator])

#Specialty
class Specialty(models.Model):
    name = models.CharField(max_length=50)
