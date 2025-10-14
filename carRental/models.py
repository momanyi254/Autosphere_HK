from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rental_cars')
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    cc = models.PositiveIntegerField(help_text="Engine capacity in cc")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Rental price per day")
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='car_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand} {self.name} ({self.year})"

    def to_dict(self):
        return {
            "id": self.id,
            "owner": self.owner.username,
            "name": self.name,
            "brand": self.brand,
            "year": self.year,
            "cc": self.cc,
            "price": str(self.price),
            "available": self.available,
            "description": self.description,
            "image": self.image.url if self.image else None,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
