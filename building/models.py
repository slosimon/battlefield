# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models

# Create your models here.

class Cost(models.Model):
	time = models.TimeField()
	days = models.IntegerField()
	oil = models.IntegerField()
	iron = models.IntegerField()
	wood = models.IntegerField()
	food = models.IntegerField()
	cost = models.IntegerField()
	culture_points = models.IntegerField()
	bonus = models.FloatField()
	level = models.IntegerField()
	def __unicode__(self):
		return unicode(self.level)

class Building(models.Model):
	cost = models.ManyToManyField(Cost)
	parliament = 'Parliament'
	summer_residence = 'Summer residence' 
	town_hall = 'Town hall' 
	headquarters = 'Headquarters' 
	shelter = 'Shelter' 
	warehouse = 'Warehouse' 
	silo = 'Silo' 
	uni = 'University'
	market = 'Market'
	camp = 'Training camp'
	ammunition = 'Ammunition workshop' 
	hangar = 'Hangar'
	railway = 'Railway' 
	port = 'Port' 
	artilery = 'Artilery mansion' 
	hero = "Hero's birth house"
	hideout = 'Hideout' 
	large_warehouse = 'Large warehouse'
	large_silo = 'Large silo'
	large_camp = 'Large camp'
	large_hangar = 'Large hangar'
	bunker = 'Bunker'
	def_line = 'Defensive line' 
	oil_refinery = 'Oil refinery'
	iron_works = 'Iron works'
	sawmill = 'Sawmill' 
	slaughter_house = 'Slaughter house' 
	can_filling_centre = 'Can filling centre'
	nuke = 'Nuke research lab'
	bazar = 'Bazar'
	options = (
		(parliament , _('Parliament')), # Palace, done
		(summer_residence , _('Summer residence')), # Residence, done
		(town_hall, _('Town hall')), # done
		(headquarters , _('Headquarters')), # Main building, done
		(shelter , _('Shelter')), # Cranny, done
		(warehouse , _('Warehouse')), # Warehouse,done
		(silo , _('Silo')), # Granary, done
		(uni , _('University')), # Academy, done
		(market , _('Market')), # Marketplace, done
		(camp , _('Training camp')), # Barracks, done
		(ammunition , _('Ammunition workshop')), # Armoury/Smithy, done
		(hangar , _('Hangar')), # Stable, done
		(railway , _('Railway')), # Tournament square, done
		(port , _('Port')), # For navy -> new thing, done
		(artilery , _('Artilery mansion')), # Workshop, done
		(hero , _("Hero's birth house")), # Hero mansion, done
		(hideout , _('Hideout')), # Treasury, done
		(large_warehouse , _('Large warehouse')), # 4 x time, cost, 3 x size, done
		(large_silo , _('Large silo')), # 4 x time, cost, 3 x size, done
		(large_camp , _('Large camp')), # done
		(large_hangar , _('Large hangar')), # done 
		(bunker , _('Bunker')), # Rally point, done
		(def_line , _('Defensive line')), # Wall, done
		(oil_refinery , _('Oil refinery')), # Bonus building for oil, done
		(iron_works , _('Iron works')), # Iron foundry, done
		(sawmill , _('Sawmill')), # Bouns building for wood, done
		(slaughter_house , _('Slaughter house')), # Food bonus buiding no.1
		(can_filling_centre , _('Can filling centre')), # Food bonus building no.2
		(bazar, _('Bazar')), # Trade center, done
		(nuke , _('Nuke research lab')), # WW, done
		# bonus buildings for each nation
	)
	name = models.CharField(max_length = 50, choices = options)
	image = models.ImageField(null = True)
	description = models.TextField(max_length = 1000)
	def __unicode__(self):
		return unicode(self.name)
	
class Field(models.Model):
	oil_field ='Oil field'
	forrest='Forrest'
	iron_mine ='Iron mine'
	farm ='Farm'
	options = (
		(oil_field , _('Oil field')),
		(forrest , _('Forrest')),
		(iron_mine , _('Iron mine')),
		(farm , _('Farm')),
	)
	name = models.CharField(max_length = 50)
	image = models.ImageField(null = True)
	description = models.TextField(max_length = 1000)
	cost = models.ManyToManyField(Cost)
	def __unicode__(self):
		return unicode(self.name)
