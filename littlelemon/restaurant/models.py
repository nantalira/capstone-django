from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', default=1)
    name = models.CharField(max_length=255)
    no_of_guest = models.IntegerField()
    bookingdate = models.DateTimeField()
    
    def __str__(self):
        return f"{self.name} - {self.bookingdate}"

class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField()
    
    def __str__(self):
        return f"{self.title} : {str(self.price)}"

