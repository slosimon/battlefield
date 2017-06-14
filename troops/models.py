# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
import world

# Create your models here.
class Resources(models.Model):
	oil = models.IntegerField(default = 750, verbose_name = _('Oil'))
	iron = models.IntegerField(default = 750, verbose_name = _('Iron'))
	wood = models.IntegerField(default = 750, verbose_name = _('Wood'))
	food = models.IntegerField(default = 750, verbose_name = _('Food'))
	
class UpgradeResources(models.Model):
	oil = models.IntegerField(default = 750, verbose_name = _('Oil'))
	iron = models.IntegerField(default = 750, verbose_name = _('Iron'))
	wood = models.IntegerField(default = 750, verbose_name = _('Wood'))
	food = models.IntegerField(default = 750, verbose_name = _('Food'))
	lvl = models.IntegerField()
	
class Troop_type(models.Model):
	infantry = 'Infantry'
	aviation = 'Aviation'
	artilery = 'Artilery'
	marine = 'Navy'
	options = (
		(infantry, _('Infantry')),
		(aviation, _('Aviation')),
		(artilery, _('Artilery')),
		(marine, _('Navy')),
	)
	typ = models.CharField(max_length = 10, choices = options)
	def __unicode__(self):
		return unicode(self.typ)
		
class Troops(models.Model):
	research_time = models.TimeField()
	research_cost = models.ForeignKey(Resources)
	training_cost = models.ForeignKey(Resources, related_name = "training_cost")
	training_time = models.TimeField()
	image = models.ImageField()
	upgrade_cost = models.ManyToManyField(UpgradeResources, null = True, related_name = "Upgrade")
	description = models.TextField(max_length = 2550)
	name = models.CharField(max_length = 25)
	consumption = models.IntegerField()
	attack_power = models.IntegerField()
	def_infantry = models.IntegerField()
	def_artilery = models.IntegerField()
	def_aviation = models.IntegerField()
	def_marine = models.IntegerField()
	troop_type = models.ForeignKey(Troop_type)
	icon = models.ImageField(blank = True, null = True, default = None)
	carry = models.IntegerField(default = 0)
	destruction_power = models.IntegerField(default = 0)
	speed = models.IntegerField(default = 0)

	


	

