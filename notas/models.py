from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Nota(models.Model):
    title = models.CharField('Título',max_length=200)
    description = models.TextField('Descripción',blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)