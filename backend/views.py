# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect

from backend.models import Template, Lead, LeadType, ActionLogs
# from scripts import startScript

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

    print files, keywords
    # startScript(files, keywords)
    return HttpResponseRedirect('/raw_leads/')


def rawLeads(request):
    raw_lead_type = LeadType.objects.get(name='raw_lead')
    leads = Lead.objects.filter(lead_type=raw_lead_type)
    return render(request, 'raw_leads.html', {'leads': leads})


def markAsGood(request):
    # Mark as good function
    ids = request.POST.get('ids')
    jd = json.dumps(ids)
    ids = eval(json.loads(jd))
    print ids
    # end of function
    return HttpResponseRedirect('/raw_leads/')


def tuncateLeads(request):
    # Delete function
    return HttpResponseRedirect('/raw_leads/')


def activeLeads(request):
    active_lead_type = LeadType.objects.get(name='active_lead')
    leads = Lead.objects.filter(lead_type=active_lead_type)
    return render(request, 'active_leads.html', {'leads': leads})


def templatesHome(request):
    return render(request, 'templates.html', {})


def makeTemplate(subject, body, name):
    body = body.encode('utf-8')
    try:
        template = Template.objects.get(name=name)
        template.body = body
        template.subject = subject
        template.save()
    except:
        template = Template(
            name=name,
            body=body,
            subject=subject,
        )
        template.save()

    return 'success'


def saveTemplate(request):
    body = request.POST['body']
    subject = request.POST['subject']
    name = request.POST['name']

    makeTemplate(subject, body, name)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def sentLeads(request):
    sent_lead_type = LeadType.objects.get(name='sent_lead')
    leads = Lead.objects.filter(lead_type=sent_lead_type)
    return render(request, 'sent_leads.html', {'leads': leads})

def logs(request):
    logs = ActionLogs.objects.all().order_by('-id')[:1000]
    return render(request, 'logs.html', {'logs': logs})
