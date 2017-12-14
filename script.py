import requests
from bs4 import BeautifulSoup as BS
from os import popen
from selenium import webdriver
import json
# from backend.models import Lead, LeadType


def saveData(dicts):
    for dict_ in dicts:
        new_lead = Lead(**dict_)
        new_lead.save()


def checkIsMobileFriendly(domain):
    url = 'https://www.googleapis.com/pagespeedonline/v3beta1/mobileReady?url=http://' + domain
    resp = requests.get(url)
    resp = resp.json()
    return resp['ruleGroups']['USABILITY']['pass']


def checkIfHasVideo(domain):
    url = 'https://' + domain
    driver = webdriver.PhantomJS()
    driver.get(url)
    soup = BS(driver.page_source, 'lxml')
    videos = soup.find_all(["embed","object","param","video", "iframe"])
    if len(videos):
        return True
    else:
        return False

def getEmail(domain):
    tube = popen('./whois.sh ' + domain)
    response = tube.read()
    return response.replace('Registrant Email:', '').lstrip().rstrip()


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


def test(url):
    from selenium.webdriver.chrome.options import Options

    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait

    import os
    import time

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.PhantomJS()
    driver.get(url)
    soup = BS(driver.page_source, 'lxml')
    divs = soup.findAll("iframe")
    print divs

    # try:
    #     element = WebDriverWait(driver, 1).until(
    #         EC.presence_of_element_located((By.ID, "page-container"))
    #     )
    #     time.sleep(100)

    #     divs = driver.findAll("iframe")
    #     print divs
    # finally:
    #     pass

    # print '--------------'

if __name__ == "__main__":
    print checkIsMobileFriendly('fplalerts.com/')
