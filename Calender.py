from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class Calender:

    @staticmethod
    def get_current_event():

        creds = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)

        now = datetime.datetime.utcnow().isoformat() + "Z"
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            return ''
        for event in events:
            timedata_now = datetime.datetime.now()
            start = str(event['start'].get('dateTime')).split('+')[0]
            start_time = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
            end = str(event['end'].get('dateTime')).split('+')[0]
            end_time = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S')

            if end_time >= timedata_now >= start_time:
                return 'Tim hat gerade folgenden Termin: ' + event['summary'] + '.'
