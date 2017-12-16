import requests
from bs4 import BeautifulSoup as BS
from os import popen
from selenium import webdriver
import json
import whois

from django.utils import timezone
from backend.models import Lead, LeadType


def saveData(dicts):
    for dict_ in dicts:
        new_lead = Lead(**dict_)
        new_lead.save()


def checkIsMobileFriendly(domain):
    try:
        url = 'https://www.googleapis.com/pagespeedonline/v3beta1/mobileReady?url=http://' + domain
        resp = requests.get(url)
        resp = resp.json()
        return resp['ruleGroups']['USABILITY']['pass']
    except:        
        url = 'https://www.googleapis.com/pagespeedonline/v3beta1/mobileReady?url=http://' + domain
        resp = requests.get(url)
        resp = resp.json()

        try:
            return resp['ruleGroups']['USABILITY']['pass']
        except:
            return -1


def checkIfHasVideo(domain, driver):
    url = 'https://' + domain

    try:
        resp = requests.get(url)
        condition = True if int(resp.status_code) == 200 else False
    except:
        condition = False

    if condition:
        driver.get(url)
    else:
        condition = True
        url = 'http://' + domain
        try:
            resp = requests.get(url)
            condition = True if int(resp.status_code) == 200 else False            
        except:
            condition = False
        if condition:
            driver.get(url)
        else:
            return -1

    soup = BS(driver.page_source, 'lxml')
    videos = soup.find_all(["embed","object","param","video", "iframe"])
    if len(videos):
        return True
    else:
        return False

def getEmail(domain):
    try:    
        emails = whois.whois(domain).emails  
        for email in emails:
            if len(email) < 30:
                return email
        return -1
    except:
        return -1
    # tube = popen('./whois.sh ' + domain)
    # response = tube.read()
    # return response.replace('Registrant Email:', '').lstrip().rstrip()


def process(keywords, zone_files):    
    driver = webdriver.PhantomJS()
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
            if checkIfHasVideo(line, driver):
                has_video = True

            mail = getEmail(line)

            if mail != -1 and has_video != -1 and has_video != -1:
                kwrds = ''
                for keyword in keywords:
                    kwrds += keyword + ' '
                dicts.append({
                    'keywords': kwrds,
                    'domain': line,
                    'mail': mail,
                    'has_video': has_video,
                    'is_mobile_friendly': is_mobile_friendly,
                    'lead_type': lead_type,
                    'datetime_of_last_change': timezone.now(),
                })

    saveData(dicts)


if __name__ == "__main__":
    print getEmail('youtube.com')
