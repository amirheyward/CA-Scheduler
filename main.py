import pandas as pd
from timeparse import timeparse

import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

df = pd.read_csv('data.csv', header=2)[:8].astype(str)
df = df.rename(columns={"Unnamed: 1": "Times"})

days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
times = df['Times'].tolist()

calendar_df = df[['Times', *days]]
# print(calendar_df.head(8))

# the object will be a person
# its fields will be a string of their name and an array containing the days and times of their shifts

name = "amir"
allshifts = [calendar_df[day].tolist() for day in days]
yourshifts = []
for i, day in enumerate(allshifts):
    yourshifts.append([days[i] + " " + times[index] for index, n in enumerate(day) if n.lower() == name])
    
# deleting day because i want to use it again
del day
yourshifts = [timeparse(shift) for day in yourshifts for shift in day]

# setting up OAuth
flow = InstalledAppFlow.from_client_secrets_file("credentials.json", ["https://www.googleapis.com/auth/calendar"]) # credentials.json excluded for safety purposes
creds = flow.run_local_server(port=0)
service = build("calendar", "v3", credentials=creds)


for start, end in yourshifts:
    event = {
        'summary': 'Shift',
        'start': {
            'dateTime': start.isoformat(timespec="milliseconds"),
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': end.isoformat(timespec="milliseconds"),
            'timeZone': 'America/New_York',
        }
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))