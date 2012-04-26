# read the FAI events from the CSV link representing the spreadsheet

CSVLINK = "https://docs.google.com/spreadsheet/pub?key=0AmJNRTRozbRcdFNtZllaNmZNQ1Zlc2FDaDREVkl4N3c&single=true&gid=0&output=csv"

import csv
from urllib import urlopen
from datetime import datetime, timedelta
from fai import Event

def get_events():
    try:
        f = urlopen(CSVLINK)
    except:
        return None
    reader = csv.DictReader(f)
    events = []
    for row in reader:
        speaker = row["Speaker Name"]
        date = row["Talk Date"]
        time = row["Talk Time"]
        title = row["Talk Title"]
        location = row["Location"]
        host = row["UTCS Host"]
        university = row["Speaker Affiliation"]
        website = row["Speaker Webpage"]
        abstract = row["Abstract"]
        bio = row["Bio"]
        curator = row["FAI curator"]
        signup = row["Schedule"]
        starttime = datetime.strptime(date + ' ' + time, '%m/%d/%Y %H:%M:%S')
        event = Event(
            date = starttime,
            location = location,
            speaker = speaker,
            title = title,
            website = website,
            university = university,
            signup = signup,
            abstract = abstract,
            bio = bio,
            host = host)
        events.append(event)
        print event

if __name__ == "__main__":
    get_events()
