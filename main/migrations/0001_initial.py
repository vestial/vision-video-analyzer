# Generated by Django 3.1.2 on 2020-10-29 19:26

from django.conf import settings
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('video',
                 models.FileField(
                     storage=django.core.files.storage.FileSystemStorage(
                         location='media/videos'),
                     upload_to='')),
                ('thumbnail',
                 models.FileField(
                     null=True,
                     storage=django.core.files.storage.FileSystemStorage(
                         location='media/thumbnails'),
                     upload_to='')),
                ('uploader',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
