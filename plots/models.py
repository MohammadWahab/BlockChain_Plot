from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

from django.db import models



class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    nid_number = models.CharField(max_length=20, unique=True)
    meta_mask_id = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'nid_number']

    def __str__(self):
        return self.email



User = get_user_model()

class Plot(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plots')
    plot_number = models.CharField(max_length=50,unique=True)
    area = models.FloatField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Plot {self.plot_number} - Owner: {self.owner.email}"


