from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils import timezone

class Status(models.TextChoices):

    PENDING = 'Pending', 'En attente'
    CONFIRMED = 'Confirmed', 'Confirmé'
    CANCELLED = 'Cancelled', 'Annulé'

class Appointment(models.Model):

    reason = models.TextField()

    prescription = models.FileField(
        upload_to='prescriptions/',
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf'],
                message="L'ordonnance doit être un fichier PDF."
            )
        ]
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    duration_minutes = models.PositiveIntegerField(
        default=30
    )

    appointment_date = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    doctor = models.ForeignKey(
        'AccountApp.Doctor',
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    patient = models.ForeignKey(
        'AccountApp.Patient',
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    def clean(self):

        super().clean()

        if self.appointment_date:

            is_new = self.pk is None

            date_changed = False

            if not is_new:
                old_appointment = Appointment.objects.get(pk=self.pk)

                date_changed = (
                    old_appointment.appointment_date
                    != self.appointment_date
                )

            if is_new or date_changed:

                if self.appointment_date <= timezone.now():

                    raise ValidationError({
                        'appointment_date':
                        "La date du rendez-vous doit être "
                        "postérieure à la date et à l'heure actuelles."
                    })

    class Meta:

        ordering = ['appointment_date']

        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'],
                name='unique_doctor_appointment_date'
            )
        ]

    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.appointment_date}"