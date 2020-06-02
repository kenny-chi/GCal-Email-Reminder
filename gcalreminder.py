
from email.mime.text import MIMEText
import base64
from base64 import urlsafe_b64encode
from googleapiclient.discovery import build
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import time
from datetime import datetime
import pytz


SENDER = 'a@gmail.com'
RECIPIENT = 'b@gmail.com'
SUBJECT = 'we did it!'
CONTENT = 'tester2'
SCOPE = 'https://www.googleapis.com/auth/calendar.events.readonly'

def initialize_credentials(scope, name):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    fileName = 'token.' + name
    if os.path.exists(fileName):
        with open(fileName, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    elif not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credential.json', scope)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(fileName, 'wb') as token:
            pickle.dump(creds, token)
    return creds


def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  encoded_message = urlsafe_b64encode(message.as_bytes())
  return {'raw': encoded_message.decode()}


def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print ('Message sent! Message Id: %s' % message['id'])
    return message
  except errors.HttpError as error:
    print ('An error occurred: %s' % error)

#service = build('gmail', 'v1', credentials=initialize_credentials())
#message = create_message(SENDER, RECIPIENT, SUBJECT, CONTENT)
#send_message(service, 'me', message)

def getCalendarEvents():
  #work on getting future events only
    page_token = None
    events = calendarservice.events().list(calendarId='primary', pageToken=page_token).execute()
    #page_token = events.get('nextPageToken')
    return events['items']

def sendEmailBeforeEvent():
    index = 0
    calendarEvents = getCalendarEvents()
    sleepTime = 1
    reminderTime = 600
    while True:
        time.sleep(sleepTime)
        event = calendarEvents[index]
        dateTime = event['start']['dateTime']
        dateTimeObj = datetime.strptime(dateTime, '%Y-%m-%dT%H:%M:%S%z')
        timeDelta = (dateTimeObj.astimezone(pytz.utc) - datetime.now(pytz.utc)).total_seconds()
        if timeDelta <= reminderTime and timeDelta > reminderTime - sleepTime * 2:
          message = create_message(SENDER, RECIPIENT, event['summary'], CONTENT)
          send_message(gmailservice, 'me', message)
        print('Event: {} | Day: {} | timeDelta(in hrs): {}'.format(event['summary'], dateTimeObj, timeDelta / 3600))
        index = (index + 1)  % len(calendarEvents)
        if index == 0:
            calendarEvents = getCalendarEvents()

def main():
  calendarservice = build('calendar', 'v3', credentials=initialize_credentials('https://www.googleapis.com/auth/calendar.events.readonly', 'cal'))
  gmailservice = build('gmail', 'v1', credentials=initialize_credentials('https://www.googleapis.com/auth/gmail.compose', 'mail'))
  sendEmailBeforeEvent()

if __name__ == '__main__':
    main()