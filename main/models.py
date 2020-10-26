from django.db import models
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User

# Create your models here.
class Video(models.Model):
    name = models.CharField(max_length=100)
    uploader = ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
