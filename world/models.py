# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
# Create your models here.

class Tribe(models.Model):
	partisan = 'Partisans'
	russian = 'Russians'
	american = 'Americans' 
	brits = 'Brittish' 
	german = 'Germans' 
	japs = 'Japanese'
	options = (
		(partisan , _('Partisans')), # Def + raiding + bouns if attacked (between gauls and teuts)
		(russian , _('Russians')), # Cheap attack + raiding (teutons like)
		(american , _('Americans')), # Hard to start, easy to end (romans like)
		(brits , _('Brittish')), # Strong def, medium wall and strong navy (between gauls and romans)
		(german , _('Germans')), # Strong attack, weak def + medium speed. Weak wall (somewhere between teuts and romans)
		(japs , _('Japanese')) # Strong in tight battles. Kamikaze (Not defined yet)
	)
	
	name = models.CharField(max_length = 20, choices = options)

class Building(models.Model):
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
	lvl = models.IntegerField(default = 0)	
		
class Center(models.Model):
	pos_01 = models.ForeignKey(Building, default = None, related_name="Typeone")
	pos_02 = models.ForeignKey(Building, default = None, related_name="Typetwo")
	pos_03 = models.ForeignKey(Building, default = None, related_name="Typethree")
	pos_04 = models.ForeignKey(Building, default = None, related_name="Typefour")
	pos_05 = models.ForeignKey(Building, default = None, related_name="Typefive")
	pos_06 = models.ForeignKey(Building, default = None, related_name="Typesix")
	pos_07 = models.ForeignKey(Building, default = None, related_name="Typeseven")
	pos_08 = models.ForeignKey(Building, default = None, related_name="Typeeight")
	pos_09 = models.ForeignKey(Building, default = None, related_name="Typenine")
	pos_10 = models.ForeignKey(Building, default = None, related_name="Typeten")
	pos_11 = models.ForeignKey(Building, default = None, related_name="Typeeleven")
	pos_12 = models.ForeignKey(Building, default = None, related_name="Typetwelve")
	pos_13 = models.ForeignKey(Building, default = None, related_name="Typethreet")
	pos_14 = models.ForeignKey(Building, default = None, related_name="Typefourt")
	pos_15 = models.ForeignKey(Building, default = None, related_name="Typefivet")
	pos_16 = models.ForeignKey(Building, default = None, related_name="Typesixt")
	pos_17 = models.ForeignKey(Building, default = None, related_name="Typesevent")
	pos_18 = models.ForeignKey(Building, default = None, related_name="Typeeightt")
	pos_19 = models.ForeignKey(Building, default = None, related_name="Typeninet")
	pos_20 = models.ForeignKey(Building, default = None, related_name="Typetwenty")

class Field(models.Model):
	oil_field ='Oil field'
	coal_mine ='Coal mine'
	iron_mine ='Iron mine'
	farm ='Farm'
	options = (
		(oil_field , _('Oil field')),
		(coal_mine , _('Coal mine')),
		(iron_mine , _('Iron mine')),
		(farm , _('Farm')),
	)
	name = models.CharField(max_length = 50)
	lvl = models.IntegerField(default = 0)
	
class Fields(models.Model):
	pos_01 = models.ForeignKey(Field, default = None, related_name="Typeone")
	pos_02 = models.ForeignKey(Field, default = None, related_name="Typetwo")
	pos_03 = models.ForeignKey(Field, default = None, related_name="Typethree")
	pos_04 = models.ForeignKey(Field, default = None, related_name="Typefour")
	pos_05 = models.ForeignKey(Field, default = None, related_name="Typefive")
	pos_06 = models.ForeignKey(Field, default = None, related_name="Typesix")
	pos_07 = models.ForeignKey(Field, default = None, related_name="Typeseven")
	pos_08 = models.ForeignKey(Field, default = None, related_name="Typeeight")
	pos_09 = models.ForeignKey(Field, default = None, related_name="Typenine")
	pos_10 = models.ForeignKey(Field, default = None, related_name="Typeten")
	pos_11 = models.ForeignKey(Field, default = None, related_name="Typeeleven")
	pos_12 = models.ForeignKey(Field, default = None, related_name="Typetwelve")
	pos_13 = models.ForeignKey(Field, default = None, related_name="Typethreet")
	pos_14 = models.ForeignKey(Field, default = None, related_name="Typefourt")
	pos_15 = models.ForeignKey(Field, default = None, related_name="Typefivet")
	pos_16 = models.ForeignKey(Field, default = None, related_name="Typesixt")
	pos_17 = models.ForeignKey(Field, default = None, related_name="Typesevent")
	pos_18 = models.ForeignKey(Field, default = None, related_name="Typeeightt")	


class Troops(models.Model):
	count = models.IntegerField(default = 0, verbose_name = _('Troops count'))
	upgrade = models.IntegerField(default = 0, verbose_name = _('Upgrade level of troops'))
	
class Army(models.Model):
	t0 = models.ForeignKey(Troops, related_name="Typeone") # Weakest troops number
	t1 = models.ForeignKey(Troops, related_name="Typetwo") # Improved troops
	t2 = models.ForeignKey(Troops, related_name="Typethree") # and so one
	t3 = models.ForeignKey(Troops, related_name="Typefour")
	t4 = models.ForeignKey(Troops, related_name="Typefive")
	t5 = models.ForeignKey(Troops, related_name="Typesix")
	t6 = models.ForeignKey(Troops, related_name="Typeseven")
	t7 = models.ForeignKey(Troops, related_name="Typeeight")
	t8 = models.ForeignKey(Troops, related_name="Typenine")
	t9 = models.ForeignKey(Troops, related_name="Typeten")
	t10 = models.ForeignKey(Troops, related_name="Typeeleven")
	t11 = models.ForeignKey(Troops, related_name="Typetwelve")
	t12 = models.ForeignKey(Troops, related_name="Typethirteen")
	t13 = models.ForeignKey(Troops, related_name="Typefourteen")
	hero = models.BooleanField(default = True)
	
class Resources(models.Model):
	oil = models.IntegerField(default = 750, verbose_name = _('Oil'))
	iron = models.IntegerField(default = 750, verbose_name = _('Iron'))
	coal = models.IntegerField(default = 750, verbose_name = _('Coal'))
	food = models.IntegerField(default = 750, verbose_name = _('Food'))
	
class Village(models.Model):
	name = models.CharField(max_length = 26)
	center = models.ForeignKey(Center) # Because every village needs it center
	fields = models.ForeignKey(Fields) # Because every village need resource fields
	location_latitude = models.IntegerField() # Because every village need co-ordinates
	location_longitude = models.IntegerField() # And two of them
	population = models.IntegerField(default = 0) # Every village should also have some inhabitants
	army = models.ForeignKey(Army) # And troops
	capital = models.BooleanField(default = True)
	resources = models.ForeignKey(Resources, related_name = "Resources")
	update = models.DateTimeField(default = datetime.now(), verbose_name = _('Last update time'))
	culture_points = models.IntegerField(default = 0)
	storage_capacity = models.IntegerField(default = 800)
	food_capacity = models.IntegerField(default = 800)
	production = models.ForeignKey(Resources, related_name = "Production")

class Update_negative(models.Model):
	empty_time = models.DateTimeField()
	village = models.ForeignKey(Village)
	
class Oasis(models.Model):
	location_latitude = models.IntegerField() # Because every oasis need co-ordinates
	location_longitude = models.IntegerField() # And two of them
	bonus_1 = models.IntegerField() # First bonus
	bonus_2 = models.IntegerField() # And possibly the seconday one
	army = models.ForeignKey(Army)
	
class Hero(models.Model):
	name = models.CharField(max_length = 50, verbose_name=_('Name')) # There are no name heroes
	experience = models.IntegerField(verbose_name = _('Hero experience'), default = 0) # And hero might get stronger after some battle
	level = models.IntegerField(verbose_name = _('Hero level'), default = 0) # And his level goes higher
	health = models.IntegerField(verbose_name=_('Health'), default = 100) # And needs to be alive
	strength = models.IntegerField(verbose_name = _('Hero strength'), default = 0) # It also have more than initial strength
	attack_bonus = models.IntegerField(verbose_name = _('Attack bonus '), default = 0) # Here comes the attack bonus
	defense_bonus = models.IntegerField(verbose_name = _('Defense bonus '), default = 0) # And defense bonus
	resources = models.IntegerField(verbose_name = _('Resource bonus'), default = 0) # And can also increase village produciton
	
class Bonus(models.Model):
	gold_club = models.BooleanField(verbose_name = _('Gold club'), default = False)
	plus_account = models.DateTimeField(verbose_name = _('Plus Account'), default = datetime.now())	
	oil_bonus_production = models.DateTimeField(verbose_name = _('Oil bonus production'), default = datetime.now())	
	iron_bonus_production = models.DateTimeField(verbose_name = _('Iron bonus production'), default = datetime.now())	
	coal_bonus_production = models.DateTimeField(verbose_name = _('Coal bonus production'), default = datetime.now())
	food_bonus_production = models.DateTimeField(verbose_name = _('Food bonus production'), default = datetime.now())	

class Defender(models.Model):
	army = models.ForeignKey(Army)
	village = models.ForeignKey(Village)
	
class Attack(models.Model):
	reinforcement = 'Reinforcement'
	full_attack = 'Full attack'
	raid = 'Raid'
	options = (
		(reinforcement , _('Reinforcement')),
		(full_attack , _('Full attack')),
		(raid , _('Raid')),
	)
	attack_type = models.CharField(max_length = 25, choices=options)
	
class Report(models.Model):
	attacker_village = models.ForeignKey(Village)
	attacker_army = models.ForeignKey(Army)
	defenders = models.ManyToManyField(Defender)
	attack_type = models.ForeignKey(Attack)
	read = models.BooleanField()
	time_stamp = models.DateTimeField()
	
class Scouting(models.Model):
	attacker_village = models.ForeignKey(Village)
	attacker_army = models.ForeignKey(Army)
	defenders = models.ManyToManyField(Defender)
	read = models.BooleanField()
	time_stamp = models.DateTimeField()

class Trading_resources(models.Model):
	oil = models.IntegerField()
	iron = models.IntegerField()
	coal = models.IntegerField()
	food = models.IntegerField()
		
class Trading(models.Model):
	sender = models.ForeignKey(Village, related_name = "Sender")
	recipent = models.ForeignKey(Village, related_name = "Recipent")
	quantity = models.ForeignKey(Trading_resources)
	time_stamp = models.DateTimeField()
	
class Medals(models.Model):
	att = 'Attack'
	defe = 'Defense'
	rai = 'Raiding'
	climb = 'Climber'
	options = (
		(att, _('%d. attacker of the week %d')),
		(defe, _('%d. defender of the week  %d')),
		(rai, _('%d. robber of the week %d')),
		(climb, _('%d. climber of the week %d')),
	)
	pos = models.IntegerField()
	week = models.IntegerField()
	medal = models.CharField(max_length = 10, choices = options)
	image = models.ImageField()
	
class Player(models.Model):
	user = models.ForeignKey(User)
	hero = models.ForeignKey(Hero)
	villages = models.ManyToManyField(Village)
	population = models.IntegerField(verbose_name = _('Population'), default = 2)
	tribe = models.ForeignKey(Tribe)
	gold = models.IntegerField(verbose_name = _('Gold'), default = 30)
	bonuses = models.ForeignKey(Bonus)
	reports = models.ManyToManyField(Report)
	scouting_reports = models.ManyToManyField(Scouting)
	market_reports = models.ManyToManyField(Trading)
	sitter_1 = models.ForeignKey(User, related_name="first_sitter", default = None)
	sitter_2 = models.ForeignKey(User, related_name="second_sitter", default = None)
	last_login = models.DateTimeField(default = datetime.now())
	artifact_holder = models.BooleanField(default = False)
	culture_points = models.IntegerField(default = 0)
	medals = models.ManyToManyField(Medals)
	old_rank = models.IntegerField()
	raided = models.IntegerField()
	attack_points = models.IntegerField()
	def_points = models.IntegerField()
	old_att = models.IntegerField()
	old_def = models.IntegerField()
	banned = models.BooleanField(default = False)
	is_active = models.BooleanField(default = False)
	activation_key = models.CharField(max_length = 25)
	
class Message(models.Model):
	sender = models.ForeignKey(Player, related_name="Sender")
	recipent = models.ForeignKey(Player, related_name="Recipent")
	content = models.TextField(max_length = 10**10)
	subject = models.CharField(max_length = 255)
	read = models.BooleanField()
	
class Troop_type(models.Model):
	infantry = 'Infantry'
	aviation = 'Aviation'
	artilery = 'Artilery'
	marine = 'Marine'
	options = (
		(infantry, _('Infantry')),
		(aviation, _('Aviation')),
		(artilery, _('Artilery')),
		(marine, _('Marine')),
	)
	typ = models.CharField(max_length = 10, choices = options)
	
class Troop(models.Model):
	name = models.CharField(max_length = 25)
	training_time_per_unit = models.IntegerField()
	cost_oil = models.IntegerField()
	cost_iron = models.IntegerField()
	cost_coal = models.IntegerField()
	cost_food = models.IntegerField()
	consumption = models.IntegerField()
	attack_power = models.IntegerField()
	def_infantry = models.IntegerField()
	def_artilery = models.IntegerField()
	def_aviation = models.IntegerField()
	def_marine = models.IntegerField()
	troop_type = models.ForeignKey(Troop_type)
	icon = models.ImageField()
	picture = models.ImageField()
	carry = models.IntegerField(default = 0)
	destruction_power = models.IntegerField(default = 0)

class Partisan_troops(models.Model):
	t0 = models.ForeignKey(Troop, related_name = "Volounteer")
	t1 = models.ForeignKey(Troop, related_name = "Senior_fighter")
	t2 = models.ForeignKey(Troop, related_name = "Hot_air_baloon")
	t3 = models.ForeignKey(Troop, related_name = "Turbo_fan_fighter")
	t4 = models.ForeignKey(Troop, related_name = "Bomber_partisan") # faster tank
	t5 = models.ForeignKey(Troop, related_name = "Fishermen_boat") # Corvette
	t6 = models.ForeignKey(Troop, related_name = "Wooden_battleship") # weaker and faster tank
	t7 = models.ForeignKey(Troop, related_name = "Carrier_partisan") # Needed for bombers if distance > 20 fields, can carry up to 20 bombers
	t8 = models.ForeignKey(Troop, related_name = "Mortar_partisan") # Weaker but faster ram
	t9 = models.ForeignKey(Troop, related_name = "Cannon_partisan") #Stronger but faster ram
	t10 = models.ForeignKey(Troop, related_name = "Tank_partisan") # Catapult alternative
	t11 = models.ForeignKey(Troop, related_name = "Heavy_tank_partisan") # Slower but stronger tank
	t12 = models.ForeignKey(Troop, related_name = "Marshall") # Chief
	t13 = models.ForeignKey(Troop, related_name = "Colonel") # Settler
	
class Russian_troops(models.Model):
	t0 = models.ForeignKey(Troop, related_name = "Soldat")
	t1 = models.ForeignKey(Troop, related_name = "Starshina")
	t2 = models.ForeignKey(Troop, related_name = "Tupolev_ANT7")
	t3 = models.ForeignKey(Troop, related_name = "MiG3")
	t4 = models.ForeignKey(Troop, related_name = "Sturmovik") # faster tank
	t5 = models.ForeignKey(Troop, related_name = "Submarine_russian") 
	t6 = models.ForeignKey(Troop, related_name = "Glorious_battleship") # weaker and faster tank
	t7 = models.ForeignKey(Troop, related_name = "Red_carrier") # Needed for bombers if distance > 20 fields, can carry up to 20 bombers
	t8 = models.ForeignKey(Troop, related_name = "Katyusha") # Weaker but faster ram
	t9 = models.ForeignKey(Troop, related_name = "Cannon_russian") #Stronger but faster ram
	t10 = models.ForeignKey(Troop, related_name = "T34") # Catapult alternative
	t11 = models.ForeignKey(Troop, related_name = "KV2") # Slower but stronger tank
	t12 = models.ForeignKey(Troop, related_name = "Generalissmus") # Chief
	t13 = models.ForeignKey(Troop, related_name = "Political_commissar") # Settler
	
	
class American_troops(models.Model):
	t0 = models.ForeignKey(Troop, related_name = "Private")
	t1 = models.ForeignKey(Troop, related_name = "Marine")
	t2 = models.ForeignKey(Troop, related_name = "DouglasO_31")
	t3 = models.ForeignKey(Troop, related_name = "Airacomet")
	t4 = models.ForeignKey(Troop, related_name = "B_17") # faster tank
	t5 = models.ForeignKey(Troop, related_name = "Submarine_american") 
	t6 = models.ForeignKey(Troop, related_name = "Great_battleship") # weaker and faster tank
	t7 = models.ForeignKey(Troop, related_name = "Carrier_american") # Needed for bombers if distance > 20 fields, can carry up to 20 bombers
	t8 = models.ForeignKey(Troop, related_name = "Mortar_american") # Weaker but faster ram
	t9 = models.ForeignKey(Troop, related_name = "Cannon_american") #Stronger but faster ram
	t10 = models.ForeignKey(Troop, related_name = "Sherman") # Catapult alternative
	t11 = models.ForeignKey(Troop, related_name = "Super_pershing") # Slower but stronger tank
	t12 = models.ForeignKey(Troop, related_name = "President") # Chief
	t13 = models.ForeignKey(Troop, related_name = "Invader") # Settler
	
class Brittish_troops(models.Model):
	t0 = models.ForeignKey(Troop, related_name = "Soldier")
	t1 = models.ForeignKey(Troop, related_name = "Royal_marine")
	t2 = models.ForeignKey(Troop, related_name = "Mosquito")
	t3 = models.ForeignKey(Troop, related_name = "Meteor")
	t4 = models.ForeignKey(Troop, related_name = "Avro_Lancaster") # faster tank
	t5 = models.ForeignKey(Troop, related_name = "HM_Submarine") 
	t6 = models.ForeignKey(Troop, related_name = "HMSB_ship") # weaker and faster tank
	t7 = models.ForeignKey(Troop, related_name = "HMSC") # Needed for bombers if distance > 20 fields, can carry up to 20 bombers
	t8 = models.ForeignKey(Troop, related_name = "Mortar_brittish") # Weaker but faster ram
	t9 = models.ForeignKey(Troop, related_name = "Cannon_brittish") #Stronger but faster ram
	t10 = models.ForeignKey(Troop, related_name = "MK6") # Catapult alternative
	t11 = models.ForeignKey(Troop, related_name = "Medium_Mark_2") # Slower but stronger tank
	t12 = models.ForeignKey(Troop, related_name = "Queen") # Chief
	t13 = models.ForeignKey(Troop, related_name = "Prime_minister") # Settler
	
class German_troops(models.Model):
	t0 = models.ForeignKey(Troop, related_name = "Wehrmacht_soldat")
	t1 = models.ForeignKey(Troop, related_name = "SS_soldat")
	t2 = models.ForeignKey(Troop, related_name = "Junkers_88D")
	t3 = models.ForeignKey(Troop, related_name = "Messerschmitt")
	t4 = models.ForeignKey(Troop, related_name = "Stuka") # faster tank
	t5 = models.ForeignKey(Troop, related_name = "U_boot") 
	t6 = models.ForeignKey(Troop, related_name = "Schiff") # weaker and faster tank
	t7 = models.ForeignKey(Troop, related_name = "F_boot") # Needed for bombers if distance > 20 fields, can carry up to 20 bombers
	t8 = models.ForeignKey(Troop, related_name = "Mortar_german") # Weaker but faster ram
	t9 = models.ForeignKey(Troop, related_name = "Cannon_german") #Stronger but faster ram
	t10 = models.ForeignKey(Troop, related_name = "Panther") # Catapult alternative
	t11 = models.ForeignKey(Troop, related_name = "Tiger") # Slower but stronger tank
	t12 = models.ForeignKey(Troop, related_name = "Fuhrer") # Chief
	t13 = models.ForeignKey(Troop, related_name = "Reich_Minister") # Settler
	
class Japanese_troops(models.Model):
	t0 = models.ForeignKey(Troop, related_name = "Warrior")
	t1 = models.ForeignKey(Troop, related_name = "Samurai")
	t2 = models.ForeignKey(Troop, related_name = "Nakajima_C6N")
	t3 = models.ForeignKey(Troop, related_name = "Kamikaze")
	t4 = models.ForeignKey(Troop, related_name = "Kawasaki_Ki48") # faster tank
	t5 = models.ForeignKey(Troop, related_name = "Submarine_japan") 
	t6 = models.ForeignKey(Troop, related_name = "Emperors_battleship") # weaker and faster tank
	t7 = models.ForeignKey(Troop, related_name = "Carrier_of_the_sun") # Needed for bombers if distance > 20 fields, can carry up to 20 bombers
	t8 = models.ForeignKey(Troop, related_name = "Mortar_japan") # Weaker but faster ram
	t9 = models.ForeignKey(Troop, related_name = "Cannon_japan") #Stronger but faster ram
	t10 = models.ForeignKey(Troop, related_name = "Ha_Go") # Catapult alternative
	t11 = models.ForeignKey(Troop, related_name = "O_I") # Slower but stronger tank
	t12 = models.ForeignKey(Troop, related_name = "Emperor") # Chief
	t13 = models.ForeignKey(Troop, related_name = "Settler") # Settler

class Queue(models.Model):
	troop = models.ForeignKey(Troop)
	quantity = models.IntegerField()
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	last_update = models.DateTimeField()
	building_lvl = models.IntegerField()
		
class Barracks(models.Model):
	queue = models.ManyToManyField(Queue)
	
class Workshop(models.Model):
	queue = models.ManyToManyField(Queue)
	
class Hangar(models.Model):
	queue = models.ManyToManyField(Queue)
	
class Port(models.Model):
	queue = models.ManyToManyField(Queue)
	
class Ally_leadership(models.Model):
	leader = models.ForeignKey(Player)
	position = models.CharField(max_length = 50, blank = True)
	mm_rights = models.BooleanField()
	diplomacy = models.BooleanField()
	
class Alliance(models.Model):
	member = models.ManyToManyField(Player)
	leadership = models.ManyToManyField(Ally_leadership)
	medals = models.ManyToManyField(Medals)
	old_population = models.IntegerField()
	
class Invitation(models.Model):
	ally = models.ForeignKey(Alliance)
	invited = models.ForeignKey(Player)
	
class Naps(models.Model):
	confirmed = models.BooleanField()
	ally_1 = models.ForeignKey(Alliance, related_name = "Ally_1")
	ally_2 = models.ForeignKey(Alliance, related_name = "Ally_2")
	
class Artifact(models.Model):
	owner = models.ForeignKey(Village)
	effect = models.IntegerField() # 1 for small, 2 for large and 3 for unique
	name = models.CharField(max_length = 50)
	activation = models.DateTimeField()
	activated  = models.BooleanField() # Could get rid of it, just to speed up and to make more garbage!
	atom = 'Atom'
	concrete = 'Concrete'
	nitro = 'Nitro'
	spy = 'Spy'
	dehydrated = 'Dehytrated'
	baby_boom = 'Baby boom'
	masterplan = 'Masterplan'
	sarin = 'Sarin'
	options = (
		(atom, _('Atom core')), # Nuke building masterplan
		(concrete, _('Reinforced concrete')), # Stability artifact 
		(nitro, _('Nytrogen')), # To speed up troops
		(spy, _('Spy')), # Scouting
		(dehydrated, _('Dehydrated food')), # Diet
		(baby_boom, _('Baby boom')), # Trainer
		(masterplan, _('Large masterplan')), # Large storage artifact
		(sarin, _('Sarin')), # Confusion
	) 
	typ = models.CharField(max_length = 15, choices = options)
	
class Artifacts(models.Model):
	arti = models.ManyToManyField(Artifact)
	
class Market_resources(models.Model):
	oil = models.IntegerField(verbose_name = _('Oil'))
	iron = models.IntegerField(verbose_name = _('Iron'))
	coal = models.IntegerField(verbose_name = _('Coal'))
	food = models.IntegerField(verbose_name = _('Food'))
	
class Market(models.Model):
	sender = models.ForeignKey(Village, related_name = "Send")
	recipent = models.ForeignKey(Village, related_name = "Get")
	quantity = models.ForeignKey(Market_resources)
	
class Market_offers(models.Model):
	sender = models.ForeignKey(Village)
	offering = models.ForeignKey(Market_resources, related_name = "Offer")
	demanding = models.ForeignKey(Market_resources, related_name = "Want")
	
