# Generated by Django 5.1.6 on 2025-03-09 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ssoweb', '0002_alter_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='province',
            field=models.CharField(max_length=25, verbose_name='استان محل سکونت'),
        ),
    ]
