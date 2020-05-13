from django.db import models

# Create your models here.
class todoview(models.Model):
    cont = models.CharField(max_length=600)
    name = models.CharField(max_length=200)
