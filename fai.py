#!/usr/bin/env python
import sys
import re
import glob
import os
from pprint import pprint
from datetime import datetime, timedelta, tzinfo
from time import strptime, localtime, sleep
import gcal # note this needs gdata-python-client to be installed as well

FILES = '/u/ai-lab/public_html/fai/2011-2012/*.txt'
NUM_FIELDS = 10

class Event:
    def __init__(self,
                 date=None,
                 coffee=None,
                 location=None,
                 speaker=None,
                 title=None,
                 website=None,
                 university=None,
                 signup=None,
                 abstract=None,
                 bio=None,
                 host=None):
        self.date = date
        self.coffee = coffee
        self.location = location
        self.speaker = speaker
        self.title = title
        self.website = website
        self.university = university
        self.signup = signup
        self.abstract = abstract
        self.bio = bio
    def subject(self):
        return 'FAI: %s - %s' % (self.speaker, self.title)
    def description(self):
        return 'ABSTRACT\n\n' + self.abstract + '\n\nABOUT THE SPEAKER:\n\n' + self.bio
    def has_passed(self):
        t = localtime()
        if t[0] > self.date[0]: # if the year has passed
            return True
        elif t[0] == self.date[0]:
            if t[1] > self.date[1]: # if the month has passed
                return True
            elif t[1] == self.date[1]:
                if t[2] > self.date[2]: # if the day has passed
                    return True
        return False
    def __str__(self):
        data = [str(self.date), str(self.coffee), self.location, self.speaker, self.title,
                self.website, self.university, self.signup, self.abstract, self.bio]
        return '\n\n'.join(data)

def read_event(file):
    (date, coffee, location, title, speaker, website, university, signup, abstract, bio) = open(file).read().replace('XXX','').split('\n\n')[:NUM_FIELDS]
    if date:
        try:
            date = strptime(date, '%B %d, %Y %I:%M%p') # "September 12, 2008, 11:00am"
        except ValueError:
            date = strptime(date, '%A, %B %d, %Y %I:%M%p') # "Friday, September 12, 2009 11:00am
    else:
        return None
    e = Event(date, coffee, location,
              speaker, title, website,
              university, signup,
              abstract, bio)
    return e

def main():
    global FILES
    if len(sys.argv) > 1:
        FILES = os.path.join(sys.argv[1],'*.txt')
    events = []
    for f in glob.glob(FILES):
        event = read_event(f)
        if event and not event.has_passed():
            print event.speaker
            events.append(event)
    calendar_service = gcal.ProgrammaticLogin()
    calendar_id = gcal.SelectCalendar(calendar_service)
    for i, event in enumerate(events):
        hour = timedelta(hours=1)
        start_time = datetime(event.date[0], event.date[1], event.date[2], event.date[3], event.date[4])
        end_time = start_time + hour
        start_time = start_time.strftime('%Y-%m-%dT%H:%M:%S.000%Z')
        end_time = end_time.strftime('%Y-%m-%dT%H:%M:%S.000%Z')
        overlapping_events = gcal.FullTextQuery(calendar_service,
                                                 calendar_id=calendar_id,
                                                 text_query = event.speaker.decode())
        for overlapping_event in overlapping_events:
            print 'deleting:', overlapping_event.title.text
            try:
                calendar_service.Delete(overlapping_event)
            except Exception, e:
                print "Google is being mean to FAI, waiting 30 s"
                sleep(30)
                calendar_service.Delete(overlapping_event)
        print 'adding:', event.subject()
        try:
            print event.location
            gcal.InsertSingleEvent(calendar_service,
                               calendar=calendar_id,
                               title = event.subject(),
                               content=event.description(),
                               where = event.location,
                               start_time = start_time,
                               end_time = end_time)
        except Exception, e:
                print "Google is being mean to FAI, waiting 30 s"
                sleep(30)
                gcal.InsertSingleEvent(calendar_service,
                               calendar=calendar_id,
                               title = event.subject(),
                               content=event.description(),
                               where = event.location,
                               start_time = start_time,
                               end_time = end_time)


if __name__ == "__main__":
    main()
