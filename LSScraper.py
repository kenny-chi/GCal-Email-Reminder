import requests
import urllib.request
from datetime import datetime
import lxml.html as lh
import time
import event as event
"""
Scraper for LearnSpeed 'Public Page URL'. 
Allows user to get all future tutoring events 
in order to email attendees at a specified time.
"""
def getCalendarEvents():
    url = ''
    #insert your LearnSpeed 'Public Page URL' here
    response = requests.get(url)
    #Create a handle, page, to handle the contents of the website
    page = requests.get(url)
    #Store the contents of the website under doc
    doc = lh.fromstring(page.content)
    #Parse data that are stored between <tr>..</tr> of HTML
    tr_elements = doc.xpath('//tr')
    events = []
    for i in range(1, len(tr_elements)):
        t = tr_elements[i]
        name = t[3].text_content()
        time = t[2].text_content()
        date = t[1].text_content()
        events.append(event.Event(name, time, date))
    return events

def main():
  [print(event) for event in getCalendarEvents()]

if __name__ == '__main__':
    main()