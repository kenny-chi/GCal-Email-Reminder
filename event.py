from datetime import datetime
class Event:
    def __init__(self, name, time, date, attendeeemail = 'a@gmail.com'):
        """
        name - String
        time - String in the format of 'HH:MM [am/pm] - HH:MM [am/pm]'
        date - String in the format of 'YYYY-MM-DD (DayOfWeek)'
        """
        self.attendee = name
        index = (date + time).rindex('-')
        dtstr = (date + time)[:index].strip()
        #format: '2020-04-13 (Mon)5:00 pm'
        self.dt = datetime.strptime(dtstr, '%Y-%m-%d (%a)%I:%M %p')
        self.attendeeemail = attendeeemail
        self.eventname = name;
        self.organizer = "me";
        print(self)

    def __str__(self):
        return '%s\t| organizer: %s\t| date: %d/%d\t| time: %d:%d' % (self.eventname[:16], self.organizer[:17], self.dt.month, self.dt.day, self.dt.hour, self.dt.minute)
    #write value function for events