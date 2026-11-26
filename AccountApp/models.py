from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    RegexValidator,
    MinLengthValidator,
)
from django.core.exceptions import ValidationError
from django.utils import timezone


phone_validator = RegexValidator(
    regex=r'^\d{8}$',
    message="Le numéro de téléphone doit contenir exactement 8 chiffres."
)

national_id_validator = RegexValidator(
    regex=r'^\d{8}$',
    message="Le numéro CIN doit contenir exactement 8 chiffres."
)


def validate_past_date(value):
    if value >= timezone.localdate():
        raise ValidationError(
            "La date de naissance doit être antérieure à aujourd'hui."
        )


# Modèle utilisateur personnalisé
class User(AbstractUser):
    pass


class Doctor(User):

    phone = models.CharField(
        max_length=8,
        validators=[phone_validator]
    )

    license_number = models.CharField(
        max_length=6,
        unique=True,
        validators=[MinLengthValidator(6)]
    )

    specialties = models.ManyToManyField(
        'Specialty',
        related_name='doctors',
        blank=True
    )

class Patient(User):

    phone = models.CharField(
        max_length=8,
        validators=[phone_validator]
    )

    birth_date = models.DateField(
        validators=[validate_past_date]
    )

    national_id = models.CharField(
        max_length=8,
        unique=True,
        validators=[national_id_validator]
    )


class Specialty(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name