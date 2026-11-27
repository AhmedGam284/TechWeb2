from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

from AccountApp.models import Doctor, Patient
# Create your models here.

#class Status(models.Model):
 #   Pending = 'PENDING' , 'En attente'
  #  Confirmed = 'CONFIRMED' , 'Confirmée'
   # Cancelled = 'CANCELLED' , 'Annulée'
class Appointment(models.Model):
    reason=models.TextField(max_length=256)
    prescription=models.FileField(blank=True ,upload_to='prescriptions/' ,validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    status=models.CharField(max_length=20,choices=[('pending','Pending'),('confirmed','Confirmed'),('cancelled','Cancelled')],default='pending')
    #status=models.CharField(max_length=20 , choices=Status.choices, default=Status.Pending)
    duaration_minutes=models.PositiveIntegerField(default=30)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    doctor=models.ForeignKey(Doctor,related_name="Appointments",on_delete=models.CASCADE)
    patient=models.ForeignKey(Patient,related_name="Appointments",on_delete=models.CASCADE)
    appointment_date=models.DateTimeField(blank=False)

    def clean(self):
        modified_date=self._state.adding or (
            Appointment.objects.filter(
                pk=self.pk,
                appointment_date=self.appointment_date
            ).exists()
        )
        if self.appointment_date <= timezone.now():
            raise ValidationError("Appointment date must be in the future.")

class Meta():
    ordering = ['-appointment_date']
    constraints = [
        models.UniqueConstraint(fields=["doctor", "appointment_date"], 
                                name="unique_appointment_per_doctor",
                                violation_error_message="This doctor already has an appointment at this date and time.")
    ]