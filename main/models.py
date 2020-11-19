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
    resolution = models.CharField(max_length=64, blank=True, null=True, default="Unknown")
    shutter_speed = models.CharField(max_length=64, blank=True, null=True, default="Unknown")
    frame_rate = models.CharField(max_length=64, blank=True, null=True, default="Unknown")
    bit_rate = models.CharField(max_length=64, blank=True, null=True, default="Unknown")
    bit_depth = models.CharField(max_length=64, blank=True, null=True, default="Unknown")
    sample_rate = models.CharField(max_length=64, blank=True, null=True, default="Unknown")
    video_length = models.DurationField(blank=True, null=True)

    def __str__(self):
        return '%s' % (self.name)

    # Returns actual file name. It should assist in dealing with videos with the same name.
    def filename(self):
        return os.path.basename(self.video.name)