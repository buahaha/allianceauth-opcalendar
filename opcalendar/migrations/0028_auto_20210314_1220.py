# Generated by Django 3.1.2 on 2021-03-14 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("opcalendar", "0027_eventvisibility_color"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventcategory",
            name="color",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Color to be displayed on calendar",
                max_length=7,
            ),
        ),
    ]
