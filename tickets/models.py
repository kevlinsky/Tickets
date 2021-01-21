from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class Ticket(models.Model):
    id = models.CharField(max_length=1000000, primary_key=True, default=uuid.uuid4, null=False, blank=False)
    qr = models.CharField(max_length=999, null=True, blank=True)
    photo = models.ImageField(upload_to='photos', null=True, blank=True)
    number = models.IntegerField(unique=True, null=True, blank=True,
                                 validators=[MaxValueValidator(999), MinValueValidator(1)])

