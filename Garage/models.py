from django.db import models
from django.contrib.auth.models import User


class Garage(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    contact = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='garages')

    def __str__(self):
        return self.name


class Service(models.Model):
    garage = models.ForeignKey(
        Garage, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    duration = models.CharField(
        max_length=50, blank=True, null=True)  # e.g. '2 hours'

    def __str__(self):
        return f"{self.name} - {self.garage.name}"


class Booking(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateField()
    time_slot = models.CharField(max_length=50)
    # pending, confirmed, cancelled
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.service.name} ({self.status})"
