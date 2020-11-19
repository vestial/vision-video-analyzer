# Generated by Django 3.1.2 on 2020-11-19 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20201119_2033'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='bit_depth_recommendation',
            field=models.TextField(blank=True, default='No recommendation available.', null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='bit_rate_recommendation',
            field=models.TextField(blank=True, default='No recommendation available.', null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='frame_rate_recommendation',
            field=models.TextField(blank=True, default='No recommendation available.', null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='resolution_recommendation',
            field=models.TextField(blank=True, default='No recommendation available.', null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='sample_rate_recommendation',
            field=models.TextField(blank=True, default='No recommendation available.', null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='shutter_speed_recommendation',
            field=models.TextField(blank=True, default='No recommendation available.', null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='video_length_recommendation',
            field=models.TextField(blank=True, default='No recommendation available.', null=True),
        ),
    ]
