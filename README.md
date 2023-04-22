# Google_OAuth2_Calendars
______________________________________


Setup guide 

```sh
pip install - r requriments.txt
python manage.py runserver
```
The server will start at port 8080.

API Specifications

To get user's credentials
```
/rest/v1/calendar/init/
```

This endpoint will be called by above endpoint after verifying credentials.
It will show all the events of user's Google Calendar
```
/rest/v1/calendar/redirect/
```

### Note: Add client_secret.json file provided by Google to run this project.
