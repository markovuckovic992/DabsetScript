# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect

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
    return render(request, 'raw_leads.html', {})


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
    return render(request, 'active_leads.html', {})


def templatesHome(request):
    return render(request, 'templates.html', {})


def makeTemplate(subject, body):
    body = body.encode('utf-8')
    template = Template(
        name=name,
        body=body,
        subject=subject,
    )
    template.save()


def makeNewTemplate(request):
    body = request.POST['body']
    subject = request.POST['subject']

    makeTemplate(subject, body)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
