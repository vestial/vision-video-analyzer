# Generated by Django 3.1.2 on 2020-11-19 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20201119_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='bit_depth',
            field=models.CharField(blank=True, default='Unknown', max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='bit_rate',
            field=models.CharField(blank=True, default='Unknown', max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='frame_rate',
            field=models.CharField(blank=True, default='Unknown', max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='resolution',
            field=models.CharField(blank=True, default='Unknown', max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='sample_rate',
            field=models.CharField(blank=True, default='Unknown', max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='shutter_speed',
            field=models.CharField(blank=True, default='Unknown', max_length=64, null=True),
        ),
    ]