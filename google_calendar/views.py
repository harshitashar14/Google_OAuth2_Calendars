from rest_framework.views import APIView
from django.http import JsonResponse
import google_auth_oauthlib.flow
import googleapiclient.discovery
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

REDIRECT_URI = 'http://127.0.0.1:8000/rest/v1/calendar/redirect/'

CLIENT_SECRET_FILE = 'google_calendar/client_secret.json'


class GoogleCalendarInitView(APIView):

    def post(self, request):
        api_flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            CLIENT_SECRET_FILE,
            scopes=SCOPES)
        api_flow.redirect_uri = REDIRECT_URI

        authorization_url, state = api_flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true')

        return JsonResponse({
            "status": "succeeded",
            "auth_url": authorization_url
        })


class GoogleCalendarRedirectView(APIView):

    def get(self, request):
        state = request.GET['state']
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            CLIENT_SECRET_FILE,
            scopes=SCOPES,
            state=state)
        flow.redirect_uri = REDIRECT_URI

        authorization_response = request.get_full_path()
        flow.fetch_token(authorization_response=authorization_response)

        creds = flow.credentials
        request.session['credentials'] = {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes}

        calendar_service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)

        events_result = calendar_service.events().list(calendarId='primary', singleEvents=True,
                                                       orderBy='startTime').execute()
        events = events_result.get('items', [])

        return JsonResponse({
            "events": events
        })
