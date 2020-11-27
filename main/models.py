from django.db import models
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
import os

fs = FileSystemStorage(location='media/videos')
thumbnails = FileSystemStorage(location='media/thumbnails')
class Video(models.Model):
    name = models.CharField(max_length=255)
    video = models.FileField(storage=fs)
    uploader = ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    thumbnail = models.FileField(storage=thumbnails, null=True)
    date_uploaded = models.DateField(auto_now=True)

    #Resolution 
    resolution = models.CharField(max_length=64, blank=True, null=True, default="Unknown")
    resolution_rating = models.CharField(max_length=64, blank=True, null=True, default="Unknown")
    resolution_recommendation = models.TextField(blank=True, null=True, default="No recommendation available.")

    #Shutter speed
    #shutter_speed = models.CharField(max_length=64, blank=True, null=True, default="Unknown")
    #shutter_speed_rating = models.CharField(max_length=64, blank=True, null=True, default="Unknown")
    #shutter_speed_recommendation = models.TextField(blank=True, null=True, default="No recommendation available.")

    #Frame rate
    frame_rate = models.CharField(max_length=64, blank=True, null=True, default="Unknown")
    frame_rate_rating = models.CharField(max_length=64, blank=True, null=True, default="Unknown")
    frame_rate_recommendation = models.TextField(blank=True, null=True, default="No recommendation available.")

    #Bit rate
    bit_rate = models.CharField(max_length=64, blank=True, null=True, default="Unknown")
    bit_rate_rating = models.CharField(max_length=64, blank=True, null=True, default="Unknown")
    bit_rate_recommendation = models.TextField(blank=True, null=True, default="No recommendation available.")

    #Bit depth
    bit_depth = models.CharField(max_length=64, blank=True, null=True, default="Unknown")
    bit_depth_rating = models.CharField(max_length=64, blank=True, null=True, default="Unknown")
    bit_depth_recommendation = models.TextField(blank=True, null=True, default="No recommendation available.")

    #Sample rate
    sample_rate = models.CharField(max_length=64, blank=True, null=True, default="Unknown")
    sample_rate_rating = models.CharField(max_length=64, blank=True, null=True, default="Unknown")
    sample_rate_recommendation = models.TextField(blank=True, null=True, default="No recommendation available.")

    #Video length
    video_length = models.CharField(max_length=64, blank=True, null=True, default="Unknown")
    video_length_rating = models.CharField(max_length=64, blank=True, null=True, default="Unknown")
    video_length_recommendation = models.TextField(blank=True, null=True, default="No recommendation available.")

    def __str__(self):
        return '%s' % (self.name)

    # Returns actual file name. It should assist in dealing with videos with the same name.
    def filename(self):
        return os.path.basename(self.video.name)