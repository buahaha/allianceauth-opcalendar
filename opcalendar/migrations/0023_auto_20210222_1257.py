# Generated by Django 3.1.6 on 2021-02-22 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opcalendar', '0022_auto_20210222_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventhost',
            name='logo_url',
            field=models.CharField(blank=True, help_text='Absolute URL for the community logo', max_length=256),
        ),
    ]
