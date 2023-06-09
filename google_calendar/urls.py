from django.urls import path
from google_calendar.views import GoogleCalendarInitView, GoogleCalendarRedirectView

urlpatterns = [
    path('init/', GoogleCalendarInitView.as_view()),
    path('redirect/', GoogleCalendarRedirectView.as_view())
]