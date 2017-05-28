# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models

# Create your models here.

class Cost(models.Model):
	time = models.TimeField()
	oil = models.IntegerField()
	iron = models.IntegerField()
	coal = models.IntegerField()
	food = models.IntegerField()
	cost = models.IntegerField()
	culture_points = models.IntegerField()
	bonus = models.IntegerField()

class Building(models.Model):
	cost = models.ForeignKey(Cost)
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
	powerplant = 'Powerplant' 
	slaughter_house = 'Slaughter house' 
	can_filling_centre = 'Can filling centre'
	nuke = 'Nuke research lab'
	options = (
		(parliament , _('Parliament')), # Palace
		(summer_residence , _('Summer residence')), # Residence
		(town_hall, _('Town hall')),
		(headquarters , _('Headquarters')), # Main building
		(shelter , _('Shelter')), # Cranny
		(warehouse , _('Warehouse')), # Warehouse
		(silo , _('Silo')), # Granary
		(uni , _('University')), # Academy
		(market , _('Market')), # Marketplace
		(camp , _('Training camp')), # Barracks
		(ammunition , _('Ammunition workshop')), # Armoury/Smithy
		(hangar , _('Hangar')), # Stable
		(railway , _('Railway')), # Tournament square
		(port , _('Port')), # For navy -> new thing
		(artilery , _('Artilery mansion')), # Workshop
		(hero , _("Hero's birth house")), # Hero mansion
		(hideout , _('Hideout')), # Treasury
		(large_warehouse , _('Large warehouse')),
		(large_silo , _('Large silo')),
		(large_camp , _('Large camp')),
		(large_hangar , _('Large hangar')),
		(bunker , _('Bunker')), # Rally point
		(def_line , _('Defensive line')), # Wall
		(oil_refinery , _('Oil refinery')), # Bonus building for oil
		(iron_works , _('Iron works')), # Iron foundry
		(powerplant , _('Powerplant')), # Bouns building for coal mine -> resource = power
		(slaughter_house , _('Slaughter house')), # Food bonus buiding no.1
		(can_filling_centre , _('Can filling centre')), # Food bonus building no.2
		(nuke , _('Nuke research lab')), # WW
		# bonus buildings for each nation
	)
	name = models.CharField(max_length = 50, choices = options)
	image = models.ImageField()
	description = models.TextField(max_length = 1000)
	
