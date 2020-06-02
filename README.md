# GCal-Email-Reminder
Utilizes Gmail, GCal, LearnSpeed API to send emails to event attendees before a meeting

*Credit to Google API Tutorials for quickstart code*

Sources: https://developers.google.com/gmail/api/quickstart/python, https://developers.google.com/calendar/quickstart/python
- Utilized APIs to compose emails with information about session start, attendees

## Mac Commands to Run Program
- Run the following command in your terminal to create a virtual environment
  - `virtualenv mypython`
- Activate your virtual environment
  - `source mypython/bin/activate`
- Install requisite dependencies
  - `pip install -r requirements.txt`
  
## To Run LearnSpeed Integration
- Add your LearnSpeed Public Page URL
- Add your email to SENDER
- `python3 gmailreminder.py`
*(Note: you may need to authorize OAuthClient2 for your Gmail Account)*
