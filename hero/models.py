# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.utils.translation import ugettext_lazy as _

class Resources(models.Model):
	oil = models.IntegerField(default = 750, verbose_name = _('Oil'))
	iron = models.IntegerField(default = 750, verbose_name = _('Iron'))
	coal = models.IntegerField(default = 750, verbose_name = _('Coal'))
	food = models.IntegerField(default = 750, verbose_name = _('Food'))
	
class Hero_revive(models.Model):
	level = models.IntegerField()
	time = models.TimeField()
	cost = models.ForeignKey(Resources)
	
class Hero_experience(models.Model):
	level = models.IntegerField()
	experience = models.IntegerField()
	
