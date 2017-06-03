# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from world.models import Troop
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Resources(models.Model):
	oil = models.IntegerField(default = 750, verbose_name = _('Oil'))
	iron = models.IntegerField(default = 750, verbose_name = _('Iron'))
	wood = models.IntegerField(default = 750, verbose_name = _('Wood'))
	food = models.IntegerField(default = 750, verbose_name = _('Food'))

class Troops(models.Model):
	troop = models.ForeignKey(Troop)
	research_time = models.TimeField()
	research_cost = models.ForeignKey(Resources)
	training_cost = models.ForeignKey(Resources, related_name = "training_cost")
	training_time = models.TimeField()
	description = models.TextField(max_length = 2550)
	def __unicode__(self):
		return unicode(self.troop)
	


	

