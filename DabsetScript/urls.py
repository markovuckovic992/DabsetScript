"""DabsetScript URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import backend.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # Backend
    url(r'^$', backend.views.home),
    url(r'^start_process/', backend.views.startProcess),
    # Raw Leads
    url(r'^raw_leads/', backend.views.rawLeads),
    url(r'^mark_as_good/', backend.views.markAsGood),
    url(r'^tuncate_leads/', backend.views.tuncateLeads),
    # Active Leads
    url(r'^active_leads/', backend.views.activeLeads),
    # Templates
    url(r'^templates/', backend.views.templatesHome),
    url(r'^make_new_template/', backend.views.makeNewTemplate),
]
