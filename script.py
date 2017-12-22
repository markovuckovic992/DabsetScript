import requests
from bs4 import BeautifulSoup as BS
from os import popen
from selenium import webdriver
import progressbar as pb
import json
import whois
import time

from django.utils import timezone
from backend.models import Lead  #, LeadType


class progress_timer:
    def __init__(self, n_iter, description="Something"):
        self.n_iter = n_iter
        self.iter = 0
        self.description = description + ': '
        self.timer = None
        self.initialize()

    def initialize(self):
        widgets = [self.description, pb.Percentage(), ' ',
                   pb.Bar(marker=pb.RotatingMarker()), ' ', pb.ETA()]
        self.timer = pb.ProgressBar(widgets=widgets, maxval=self.n_iter).start()

    def update(self, q=1):
        self.timer.update(self.iter)
        self.iter += q

    def finish(self):
        self.timer.finish()

def saveData(dicts):
    for dict_ in dicts:
        new_lead = Lead(**dict_)
        new_lead.save()


def checkIsMobileFriendly(domain):
    # try:
    #     url = 'https://www.googleapis.com/pagespeedonline/v3beta1/mobileReady?url=http://' + domain
    #     resp = requests.get(url)
    #     resp = resp.json()
    #     return resp['ruleGroups']['USABILITY']['pass']
    # except:
    url = 'https://www.googleapis.com/pagespeedonline/v3beta1/mobileReady?url=http://' + domain
    resp = requests.get(url)
    resp = resp.json()

    try:
        return resp['ruleGroups']['USABILITY']['pass']
    except:
        return -1


def checkIfHasVideo(domain, driver):
    url = 'http://' + domain

    try:
        resp = requests.get(url)
        condition = True if int(resp.status_code) == 200 else False
    except:
        condition = False

    # if condition:
    #     pass
    #     # try:
    #     #     driver.get(url)
    #     # except:
    #     #     return -1
    # else:
    #     condition = True
    #     url = 'https://' + domain
    #     try:
    #         resp = requests.get(url)
    #         condition = True if int(resp.status_code) == 200 else False
    #     except:
    #         condition = False

    if condition:
        try:
            driver.get(url)
        except:
            return -1
    else:
        return -1

    if not condition:
        return -1

    soup = BS(driver.page_source, 'lxml')
    # soup = BS(resp.content, 'lxml')
    videos = soup.find_all(["embed", "object", "param", "video", "iframe"])
    if len(videos):
        return True
    else:
        return False


def getEmail(domain):
    try:
        emails = whois.whois(domain).emails
        if '@' in emails:
            return emails
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

    start_time = time.time()
    driver = webdriver.PhantomJS()
    # lead_type = LeadType.objects.get(name="raw_lead")
    dicts = []

    for file in zone_files:
        keywords = sorted(keywords, key=len, reverse=True)
        tube = popen('./getLines.sh ' + file + ' ' + keywords[0])
        matched_lines = set(tube.read().split())
        tube.close()

        if len(keywords) > 1:
            for keyword in keywords[1:]:
                matched_lines = [line.lower() for line in matched_lines if keyword.lower() in line.lower()]

        print '--------------------------\n', str(len(matched_lines)), '\n--------------------------'
        pt = progress_timer(description='process: ', n_iter=len(matched_lines))
        for line in matched_lines:
            # mail = ''
            mail = getEmail(line)
            if mail == -1:
                pt.update()
                continue
            # is_mobile_friendly = True
            is_mobile_friendly = checkIsMobileFriendly(line)
            if is_mobile_friendly == -1:
                pt.update()
                continue
            # has_video = True
            has_video = checkIfHasVideo(line, driver)
            if has_video == -1:
                pt.update()
                continue

            kwrds = ''
            for keyword in keywords:
                kwrds += keyword + ' '
            dicts.append({
                'keywords': kwrds,
                'domain': line,
                'mail': mail,
                'has_video': has_video,
                'is_mobile_friendly': is_mobile_friendly,
                # 'lead_type': lead_type,
                'datetime_of_last_change': timezone.now(),
            })
            pt.update()

    saveData(dicts)

    print '--------------------------\n', (time.time() - start_time), '\n--------------------------'


if __name__ == "__main__":
    print checkIfHasVideo('funnelexpert.com')
