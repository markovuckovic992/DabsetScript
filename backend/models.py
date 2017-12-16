# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.
class Template(models.Model):
    name = models.CharField(max_length=10)
    subject = models.CharField(max_length=25)
    body = models.CharField(max_length=300)

    class Meta:
        db_table = "templates"


class LeadType(models.Model):
    name = models.CharField(max_length=15)

    class Meta:
        db_table = "lead_types"


class Lead(models.Model):
    keywords = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    mail = models.CharField(max_length=100, blank=True, null=True)
    has_video = models.SmallIntegerField(default=0)
    is_mobile_friendly = models.SmallIntegerField(default=0)

    lead_type = models.ForeignKey(LeadType)
    template = models.ForeignKey(Template, blank=True, null=True)
    sent_count = models.SmallIntegerField(default=0)
    date = models.DateField(default=timezone.now)
    datetime_of_last_change = models.DateTimeField(default=None)

    class Meta:
        db_table = "leads"

    def save(self, *args, **kw):
        if self.pk is not None:
            orig = Lead.objects.get(pk=self.pk)
            field_names = [field.name for field in Lead._meta.fields]
            fields_stats = {}
            for field_name in field_names:
                if "%s" % getattr(orig, field_name) != "%s" % getattr(self, field_name) and field_name != 'datetime_of_last_change':
                    try:
                        ActionLogs(
                            lead=self,
                            field_thats_changed=field_name,
                            old_value=getattr(orig, field_name),
                            new_value=getattr(self, field_name),
                        ).save()
                    except:
                        pass
        super(Lead, self).save(*args, **kw)


class ActionLogs(models.Model):
    lead = models.ForeignKey(Lead)
    field_thats_changed = models.CharField(max_length=25)
    old_value = models.CharField(max_length=100)
    new_value = models.CharField(max_length=100)

    class Meta:
        db_table = "action_logs"


