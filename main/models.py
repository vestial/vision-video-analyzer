from django.db import models
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
import os

fs = FileSystemStorage(location='media/videos')

class Video(models.Model):
    name = models.CharField(max_length=255)
    video = models.FileField(storage=fs)
    uploader = ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.name)

    # Returns actual file name. It should assist in dealing with videos with the same name.
    def filename(self):
        return os.path.basename(self.video.name)