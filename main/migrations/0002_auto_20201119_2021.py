# Generated by Django 3.1.2 on 2020-11-19 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='bit_depth',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='bit_rate',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='date_uploaded',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='video',
            name='frame_rate',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='resolution',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='sample_rate',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='shutter_speed',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='video_length',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
