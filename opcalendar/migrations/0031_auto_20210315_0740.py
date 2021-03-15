# Generated by Django 3.1.2 on 2021-03-15 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opcalendar', '0030_ingameevents_event_owner_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='general',
            options={'default_permissions': (), 'managed': False, 'permissions': (('basic_access', 'Can access this app and see operations based on visibility rules'), ('view_ingame_events', 'Can see personal and corporation ingame events'), ('view_ingame_alliance_events', 'Can see own alliance ingame events'), ('view_ingame_all_events', 'Can see all ingame events'), ('create_event', 'Can create and edit events'), ('manage_event', 'Can delete and manage signups'), ('add_ingame_calendar_owner', 'Can add ingame calendar feeds for their corporation'))},
        ),
    ]
