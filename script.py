import requests
from bs4 import BeautifulSoup as BS
from os import popen
from backend.models import Lead, LeadType


def saveData(dicts):
    for dict_ in dicts:
        new_lead = Lead(**dict_)
        new_lead.save()


def checkIsMobileFriendly(domain):
    url = 'http://' + domain
    resp = requests.get(url)
    resp = resp.json()
    return resp['is_mobile_friendly']


def checkIfHasVideo(domain):
    url = 'http://' + domain
    resp = requests.get(url)
    soup = BS(page.content)
    videos = soup.find_all("video")

    if len(video):
        return True
    else:
        return False

def getEmail(domain):
    tube = popen('./whois.sh ' + domain)
    return tube.read()

def process(keywords, zone_files):
    lead_type = LeadType.objects.get(name="raw_lead")
    dicts = []

    for file in zone_files:
        keywords = sorted(keywords, key=len, reverse=True)
        tube = popen('./getLines.sh ' + file + ' ' + keywords[0])
        matched_lines = set(tube.read().split())
        tube.close()

        if len(keywords) > 1:
            for keyword in keywords[1:]:
                matched_lines = [line.lower() for line in matched_lines if keyword.lower() in line.lower()]

        for line in matched_lines:
            is_mobile_friendly = False
            has_video = False
            if checkIsMobileFriendly(line):
                is_mobile_friendly = True
            if checkIfHasVideo(line):
                has_video = True

            mail = getEmail(line)
            dicts.append({
                'keywords': keywords,
                'domain': line,
                'mail': mail,
                'has_video': has_video,
                'is_mobile_friendly': is_mobile_friendly,
                'lead_type': lead_type,
                'datetime_of_last_change': timezone.now(),
            })

    saveData(dicts)
