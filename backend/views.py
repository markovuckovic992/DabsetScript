# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
import itertools

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse

from backend.models import Template, Lead, LeadType, ActionLogs
from script import process
from custom_email import customEmail

def home(request):
    return render(request, 'index.html', {})


def startProcess(request):
    files = []
    keywords = []

    for key in request.FILES.keys():
        fs = FileSystemStorage()
        if fs.exists(request.FILES[key].name):
            fs.delete(request.FILES[key].name)
        fs.save(request.FILES[key].name, request.FILES[key])
        files.append(request.FILES[key].name)

    kws = request.POST['keywords'].split(',')
    for kw in kws:
        keywords.append(''.join(kw.split()))

    # print files, keywords
    process(keywords, files)
    return HttpResponse('sucess')


def Leads(request):
    if 'date' in request.GET:
        date = datetime.strptime(request.GET['date'], '%d-%m-%Y')
    else:
        date = datetime.now().date()
    # raw_lead_type = LeadType.objects.get(name='raw_lead')
    leads = Lead.objects.filter(date=date)
    return render(request, 'leads.html', {'leads': leads})


def markAsGood(request):
    # Mark as good function
    name_of_campaign = request.POST.get('name_of_campaign')
    ids = request.POST.get('ids')
    jd = json.dumps(ids)
    ids = eval(json.loads(jd))
    # end of function
    leads = Lead.objects.filter(id__in=ids)
    campaign = Campaign(
        name=name_of_campaign,
    ).save()

    ids = set(lead.id for lead in leads)
    leads = itertools.ifilter(lambda x: x.id not in ids, leads)
    campaign.add(*leads)
    campaign.save()
    # lead_type = LeadType.objects.get(name='active_lead')
    # Lead.objects.filter(id__in=ids).update(lead_type=lead_type)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def tuncateLeads(request):
    if 'date' in request.POST:
        date = datetime.strptime(request.POST['date'], '%d-%m-%Y')
    else:
        date = datetime.now().date()
    lead_type = LeadType.objects.get(name=request.POST['lead_type'])

    Lead.objects.filter(date=date, lead_type=lead_type).delete()
    return HttpResponse('sucess')


def Campaigns(request):
    campaigns = Campaign.objects.all()
    return render(request, 'campaigns.html', {'campaigns': campaigns})


def templatesHome(request):
    if 'template_id' in request.GET:
        template = Template.objects.get(id=request.GET['template_id'])
    else:
        template = {}
    templates = Template.objects.all()
    return render(request, 'templates.html', {'templates': templates, 'template': template})


def makeTemplate(subject, body, name):
    body = body.encode('utf-8')
    template = Template(
        name=name,
        body=body,
        subject=subject,
    )
    template.save()

    return 'success'

def updateTemplate(subject, body, name, id):
    template = Template.objects.get(id=id)
    template.name = name
    template.body = body
    template.subject = subject
    template.save()

    return 'success'

def saveTemplate(request):
    body = request.POST['body']
    subject = request.POST['subject']
    name = request.POST['name']
    id = int(request.POST['id'])

    if id != 0:
        updateTemplate(subject, body, name, id)
    else:
        makeTemplate(subject, body, name)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def sentLeads(request):
    sent_lead_type = LeadType.objects.get(name='sent_lead')
    leads = Lead.objects.filter(lead_type=sent_lead_type)
    return render(request, 'sent_leads.html', {'leads': leads})


def logs(request):
    logs = ActionLogs.objects.all().order_by('-id')[:1000]
    return render(request, 'logs.html', {'logs': logs})


def sendCampaign(request):
    ids = request.POST.get('ids')
    jd = json.dumps(ids)
    ids = eval(json.loads(jd))

    leads = Lead.objects.filter(id__in=ids)
    campaign_log = CampaignLog(
        campaign_id=campaign_id,
        template_name=template_name,
    ).save()

    ids = set(lead.id for lead in leads)
    leads = itertools.ifilter(lambda x: x.id not in ids, leads)
    campaign_log.add(*leads)

    campaign_log.save()


def sendEmails(request):
    smtpSender = customEmail()
    ids = request.POST.get('ids')
    jd = json.dumps(ids)
    ids = eval(json.loads(jd))

    for _id in ids:
        lead = Lead.objects.get(id=_id)
        smtpSender.sendEmail(lead.mail, lead.template)

    smtpSender.close()
