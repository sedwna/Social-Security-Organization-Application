# Generated by Django 5.1.6 on 2025-03-09 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ssoweb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='code',
            field=models.CharField(max_length=4),
        ),
    ]
