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
import LSScraper as ls
import event as e

class GmailReminder:
    def __init__(self, sender, events, time):
        """
        sender - sender's email
        events - list of Event objects
        time - reminder time (in minutes before event)
        """
        self.sender = sender
        for event in events:
            if not isinstance(event, e.Event):
                raise ValueError
        self.events = events
        self.time = time
        #need to sort events by time
        #make sure all events are in the future

    def initialize_credentials(self, scope, name):
        creds = None
        # The file token.[name] stores the user's access and refresh tokens, and is
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

    def create_message(self, sender, to, subject, message_text):
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

    def send_message(self, service, user_id, message):
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

    def sendEmailBeforeEvent(self):
        gmailservice = build('gmail', 'v1', credentials=self.initialize_credentials('https://www.googleapis.com/auth/gmail.compose', 'mail'))
        while True:
            event = self.events[0]
            dateTime = event.dt
            timeDelta = (dateTime.astimezone(pytz.utc) - datetime.now(pytz.utc)).total_seconds()
            if (timeDelta > self.time * 60):
                time.sleep(timeDelta - self.time * 60)
            reminder = '%s, you have a reminder for a meeting starting in %d minutes. ' % (event.attendee, self.time)
            message = self.create_message(self.sender, event.attendeeemail, event.attendee, reminder)
            self.send_message(gmailservice, 'me', message)
            self.events.remove(event)
            #print('Event: {} | Day: {} | Hours until event: {}'.format(event.attendee, dateTime, timeDelta / 3600))

def main():
    SENDER = 'a@gmail.com'
    lsremind = GmailReminder(SENDER, ls.getCalendarEvents(), 5)
    lsremind.sendEmailBeforeEvent()
    #send email to organizer as a reminder

if __name__ == '__main__':
    main()