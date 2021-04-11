# Operation Calendar

An operation calendar app for Alliance Auth to display fleet operations and other events.

![release](https://img.shields.io/pypi/v/aa-opcalendar??label=release) ![python](https://img.shields.io/pypi/pyversions/aa-opcalendar?) ![license](https://img.shields.io/badge/license-MIT-green)

## Includes:
 * Calendar type view of different events
 * Manual events
 	* User created
 	* Defailed view
 	* Ical feed for exporting events
* Public NPSI events
 	* Automatic syncing with supported NPSI community events over APIs
* Ingame events
	* Automatic syncing with ingame events
	* Supports moon mining calendar events
	* Personal, Corporation and Alliance calendars
* Supports [structure timers](https://gitlab.com/ErikKalkoken/aa-structuretimers)
* Event visibility options
	* Custom names
	* Restrict to groups
	* Restrict to states
* Event categories
 	* Custom names
 	* Custom tickers
 	* Custom colors
* Multihost support
* Discord notifications
	* Webhook
	* For: new, edited and deleted events


![screenshot](https://i.imgur.com/bLepJGH.jpg)

## Installation
 1. Install the Repo `pip install aa-opcalendar`
 2. Add `'opcalendar',` to your `INSTALLED_APPS` in your projects `local.py`
 3. Run migrations `python manage.py migrate`
 4. Collect static files `python manage.py collectstatic`
 5. Restart supervisor `supervisorctl reload myauth:`
 6. Setup permissions

## Permissions

Perm | Auth Site | Example Target Group
 --- | --- | ---
opcalendar basic_access | Can access this app and see operations based on visibility rules | Everyone
opcalendar create_event | Can create and edit events | Leadership, FCs
opcalendar manage_event | Can delete and manage signups | Leadership, FCs
opcalendar see_signups | Can see all signups for event | Leadership, FCs, Members

## Settings

Name | Description | Default
 --- | --- | ---
OPCALENDAR_NOTIFY_IMPORTS | Wheter to send out discord notifications for ingame and public NPSI events | True
OPCALENDAR_DISPLAY_STRUCTURETIMERS | whether we should inculde timers from the structuretimers plugin in the calendar | True
OPCALENDAR_DISPLAY_MOONMINING | whether we should inculde extractions from the aa-moonmining plugin in the calendar | True
OPCALENDAR_DISCORD_OPS_DISPLAY_EXTERNAL | whether we display external hosts such as ingame hosts in the discord ops command filters | False

## Setup
Before you are able to create new events on the front end you will need to setup the needed categories and visibility filters for your events.

### 1. Host
Hosts are for identifying reasons. If you run a single corporation or alliance entity you most likely only want one host. If you want to extend the calendar with other hosts such as NPSI communities you can create a host for each different entity.
- Host name is shown on the event and on discord notifications
- You can customize host logos
- Go to the admin site

### 2. Visibility filter
These filters will determine who is able to see the events that are labeled with each different visibility filter.
- Can be restricted to groups and states
- If no groups or states are selected the events will be visible for everyone
- You can determine a custom color tag that will be shown on the top right corner of the event
- Each visibility filter will be displayed on the calendar and can be used for filtering events on the calendar
- Discord notification webhooks can be assigned for each visibility filter. Events created, deleted or edited under this filter will then be sent over to discord.

### 3. Categories
Categories are displayed as a ticker infront of manually created events. Most common categories are: PvP, Stratop, Mining, CTA etc...
- Ticker displayed on event
- Custom colors

### 4. Discord webhook
If you want to receive notifications about your events (created/modified/deleted) on your discord you can add a webhook for the channel in discord you want to receive the notifications to. The webhooks you create will be used in the visibility filters.

## Adding manual events
To add a manual event simply go to the calendar page and press on the new event button. Fill in and select the needed information.


## Importing NPSI fleets
Opcalendar has  the ability to import predetermined NPSI fleets directly into your calendar.

### Supported NPSI communities
Opcalendar is currently supporting imports for the following NPSI fleets:

- Spectre fleet
- Eve University (classes only)
- FUN INC

### Setup

- **Go to admin panel and select NPSI Event Imports**
- **Create a host** for each import and fill in the needed details for them.
- **Add a new import** by pressing on the add event import button
- **Select the source** where you want to fetch the fleets.
- **Determine operation type** for each fetched fleet.
- **Determine operation visibility** for each fetched fleet.

To schedule the import runs either add the following line in your local.py file or set up a perioduc task for the `opcalendar.tasks.import_all_npsi_fleets` task on your admin menu to fetch fleets every hour.

```
CELERYBEAT_SCHEDULE['import_all_npsi_fleets'] = {
    'task': 'opcalendar.tasks.import_all_npsi_fleets',
    'schedule': crontab(minute=0, hour='*'),
}

```

## Importing fleets from ingame calendar
You can import events that have been created in the ingame calendar. As the fields on the ingame calendar are limited the events will not be as detailed as when created directly from the calendar.

1. Give the `add_ingame_calendar_owner` role for the wanter groups
2. Navigate to the opcalendar page and press the `Add Ingame Calendar Feed` button
3. Log in with the character that holds the calendar
5. Add the following line into your local.py setting file or set up a periodic task for the `opcalendar.tasks.update_all_ingame_events` to pull fleets from ingame every 5 minutes.

```
CELERYBEAT_SCHEDULE['update_all_ingame_events'] = {
    'task': 'opcalendar.tasks.update_all_ingame_events',
    'schedule': crontab(minute='*/5'),
}
```

### Ingame event visibility and categories
On default the ingame events you import have no visibility filter and no category. This means they will be visible for everyone.

If you wish to add a visibility filter or a category similar to the manual events simply go to the `admin panel -> Ingame event owners` and select a filter and a category for the owner.

After selecing a visibility filter and a category the ingame events will behave similar to the manual events and respect the group and state restrictions set for the visibility filters.

### Ical feed setup (optional)
Opcalendar has the ability to generate a standard ical formated feed for pushing out events. To push out evets to the feed without login requirement requires editing the allianceauth url file as on default all pages are locked behind a login requirement.

#### Feed setup
1. Open up the event visibility category and check the box to include it in the ical feed.
2. Open the alliance auth `urls.py` file that is located on default in the following path `/home/allianceserver/myauth/myauth/urls.py`
3. On default the file looks something like this:
```
from django.conf.urls import include, url
from allianceauth import urls

urlpatterns = [
    url(r'', include(urls)),
]

handler500 = 'allianceauth.views.Generic500Redirect'
handler404 = 'allianceauth.views.Generic404Redirect'
handler403 = 'allianceauth.views.Generic403Redirect'
handler400 = 'allianceauth.views.Generic400Redirect'
```
4. Include the following 2 lines in the file:
	- `from opcalendar.views import EventFeed #Added import for opcalendar ical feed` bellow the imports on top of the file
	- `url(r'^opcalendar/feed.ics', EventFeed()), #Opcalendar feed url` in the `urlpatterns` **before** the `url(r'', include(urls)),` line
Your file `urls.py` file should now look like this:
```
from django.conf.urls import include, url
from allianceauth import urls
from opcalendar.views import EventFeed #Added import for opcalendar ical feed

urlpatterns = [
    url(r'^opcalendar/feed.ics', EventFeed()), #Opcalendar feed url
    url(r'', include(urls)),
]

handler500 = 'allianceauth.views.Generic500Redirect'
handler404 = 'allianceauth.views.Generic404Redirect'
handler403 = 'allianceauth.views.Generic403Redirect'
handler400 = 'allianceauth.views.Generic400Redirect'
```
5. You can now access the ical feed at `auth.example.com/opcalendar/feed.ics`

## Contributing
Make sure you have signed the [License Agreement](https://developers.eveonline.com/resource/license-agreement) by logging in at https://developers.eveonline.com before submitting any pull requests. All bug fixes or features must not include extra superfluous formatting changes.
