# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
import building
import troops
from django.conf import settings

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
	def __unicode__(self):
		return unicode(self.name)

class Building(models.Model):
	building = models.ForeignKey('building.Building', null = True)
	lvl = models.IntegerField(default = 0)
	
		
class Center(models.Model):
	pos_01 = models.ForeignKey(Building, default = None, null = True, related_name="Typeone")
	pos_02 = models.ForeignKey(Building, default = None, null = True, related_name="Typetwo")
	pos_03 = models.ForeignKey(Building, default = None, null = True, related_name="Typethree")
	pos_04 = models.ForeignKey(Building, default = None, null = True, related_name="Typefour")
	pos_05 = models.ForeignKey(Building, default = None, null = True, related_name="Typefive")
	pos_06 = models.ForeignKey(Building, default = None, null = True, related_name="Typesix")
	pos_07 = models.ForeignKey(Building, default = None, null = True, related_name="Typeseven")
	pos_08 = models.ForeignKey(Building, default = None, null = True, related_name="Typeeight")
	pos_09 = models.ForeignKey(Building, default = None, null = True, related_name="Typenine")
	pos_10 = models.ForeignKey(Building, default = None, null = True, related_name="Typeten")
	pos_11 = models.ForeignKey(Building, default = None, null = True, related_name="Typeeleven")
	pos_12 = models.ForeignKey(Building, default = None, null = True, related_name="Typetwelve")
	pos_13 = models.ForeignKey(Building, default = None, null = True, related_name="Typethreet")
	pos_14 = models.ForeignKey(Building, default = None, null = True, related_name="Typefourt")
	pos_15 = models.ForeignKey(Building, default = None, null = True, related_name="Typefivet")
	pos_16 = models.ForeignKey(Building, default = None, null = True, related_name="Typesixt")
	pos_17 = models.ForeignKey(Building, default = None, null = True, related_name="Typesevent")
	pos_18 = models.ForeignKey(Building, default = None, null = True, related_name="Typeeightt")
	pos_19 = models.ForeignKey(Building, default = None, null = True, related_name="Typeninet")
	pos_20 = models.ForeignKey(Building, default = None, null = True, related_name="Typetwenty")
	pos_21 = models.ForeignKey(Building, default = None, null = True, related_name="Typeto")
	pos_22 = models.ForeignKey(Building, default = None, null = True, related_name="Typett")
	pos_23 = models.ForeignKey(Building, default = None, null = True, related_name="Typetth")
	pos_24 = models.ForeignKey(Building, default = None, null = True, related_name="Typetf")

class Field(models.Model):
	name = models.ForeignKey('building.Field', null = True)
	lvl = models.IntegerField(default = 0)

		
class VillageType(models.Model):
	oil_field = models.IntegerField()
	forrest = models.IntegerField()
	iron_mine = models.IntegerField()
	farm = models.IntegerField()
	
	
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
	oil = models.FloatField(default = 750, verbose_name = _('Oil'))
	iron = models.FloatField(default = 750, verbose_name = _('Iron'))
	wood = models.FloatField(default = 750, verbose_name = _('Wood'))
	food = models.FloatField(default = 750, verbose_name = _('Food'))
	
class FieldQueue(models.Model):
	field = models.ForeignKey(Field)
	to = models.IntegerField()
	start = models.DateTimeField(null = True, default = None)
	end = models.DateTimeField()
	
class BuildingQueue(models.Model):
	building = models.ForeignKey(Building)
	to = models.IntegerField()
	start = models.DateTimeField(null = True, default = None)
	end = models.DateTimeField()
	
class Troop(models.Model):
	troop = models.ForeignKey('troops.Troops', null = True)
	lvl = models.IntegerField(default = 0)

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
	next_update = models.DateTimeField(default = datetime.now())
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
	
class TrainingQueue(models.Model):
	barracks = models.ForeignKey(Barracks, null = True, default = None)
	workshop = models.ForeignKey(Workshop, null = True, default = None)
	hangar = models.ForeignKey(Hangar, null = True, default = None)
	port = models.ForeignKey(Port, null = True, default = None)
	barracks_large = models.ForeignKey(Barracks,related_name = 'Large', null = True, default = None)
	hangar_large = models.ForeignKey(Hangar, related_name = 'Large', null = True, default = None)
	next_update = models.TimeField(default = None, null = True)
	
class Village(models.Model):
	typ = models.ForeignKey(VillageType)
	name = models.CharField(max_length = 26, null = True)
	center = models.ForeignKey(Center, null = True) # Because every village needs it center
	fields = models.ForeignKey(Fields, null = True) # Because every village need resource fields
	location_latitude = models.IntegerField(null = True) # Because every village need co-ordinates
	location_longitude = models.IntegerField(null = True) # And two of them
	population = models.IntegerField(default = 0) # Every village should also have some inhabitants
	army = models.ForeignKey(Army, null = True) # And troops
	capital = models.BooleanField(default = True)
	resources = models.ForeignKey(Resources, related_name = "Resources", null = True)
	update = models.DateTimeField(default = datetime.now(), verbose_name = _('Last update time'), null = True)
	culture_points = models.IntegerField(default = 0)
	storage_capacity = models.IntegerField(default = 800)
	food_capacity = models.IntegerField(default = 800)
	production = models.ForeignKey(Resources, related_name = "Production", null = True)
	reinforcements = models.ManyToManyField(Army, related_name="reinforcements", null = True)
	field_1 = models.ForeignKey(FieldQueue,default = None, null = True)
	field_2 = models.ForeignKey(FieldQueue, default = None, null = True, related_name = 'Secondary')
	building_1 = models.ForeignKey(BuildingQueue, default = None, null = True)
	building_2 = models.ForeignKey(BuildingQueue, default = None, null = True, related_name = 'Secondary')
	next_update = models.DateTimeField(default = None, null = True) 
	real_production = models.ForeignKey(Resources, related_name = 'real', null = True, default = None)
	bonus = models.ForeignKey(Resources, related_name = 'bonus', null = True, default = None)
	free_crop = models.IntegerField()
	training_queue = models.ForeignKey(TrainingQueue, null = True, default = None)

class Update_negative(models.Model):
	empty_time = models.DateTimeField()
	village = models.ForeignKey(Village)
	
class Hero(models.Model):
	name = models.CharField(max_length = 50, verbose_name=_('Name')) # There are no name heroes
	experience = models.IntegerField(verbose_name = _('Hero experience'), default = 0) # And hero might get stronger after some battle
	level = models.IntegerField(verbose_name = _('Hero level'), default = 0) # And his level goes higher
	health = models.IntegerField(verbose_name=_('Health'), default = 100) # And needs to be alive
	strength = models.IntegerField(verbose_name = _('Hero strength'), default = 100) # It also have more than initial strength
	attack_bonus = models.IntegerField(verbose_name = _('Attack bonus '), default = 0) # Here comes the attack bonus
	defense_bonus = models.IntegerField(verbose_name = _('Defense bonus '), default = 0) # And defense bonus
	gold_bonus = models.IntegerField(verbose_name = _('Gold bonus'), default = 0)
	resources = models.IntegerField(verbose_name = _('Resource bonus'), default = 0) # And can also increase village produciton
	
class Bonus(models.Model):
	gold_club = models.BooleanField(verbose_name = _('Gold club'), default = False)
	plus_account = models.DateTimeField(verbose_name = _('Plus Account'), default = datetime.now())	
	oil_bonus_production = models.DateTimeField(verbose_name = _('Oil bonus production'), default = datetime.now())	
	iron_bonus_production = models.DateTimeField(verbose_name = _('Iron bonus production'), default = datetime.now())	
	wood_bonus_production = models.DateTimeField(verbose_name = _('Wood bonus production'), default = datetime.now())
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
	def __unicode__(self):
		return unicode(self.attack_type)
        
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
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	hero = models.ForeignKey(Hero)
	villages = models.ManyToManyField(Village, null=True)
	population = models.IntegerField(verbose_name = _('Population'), default = 2)
	tribe = models.ForeignKey(Tribe)
	gold = models.IntegerField(verbose_name = _('Gold'), default = 30)
	bonuses = models.ForeignKey(Bonus)
	reports = models.ManyToManyField(Report, null = True)
	scouting_reports = models.ManyToManyField(Scouting, null = True)
	market_reports = models.ManyToManyField(Trading, null = True)
	sitter_1 = models.ForeignKey(User, related_name="first_sitter", default = None, null = True)
	sitter_2 = models.ForeignKey(User, related_name="second_sitter", default = None, null = True)
	last_login = models.DateTimeField(default = datetime.now())
	artifact_holder = models.BooleanField(default = False)
	culture_points = models.FloatField(default = 0)
	last_update = models.DateTimeField(null = True, default = None)
	medals = models.ManyToManyField(Medals, null = True)
	old_rank = models.IntegerField()
	raided = models.IntegerField(default = 0)
	attack_points = models.IntegerField(default = 0)
	def_points = models.IntegerField(default = 0)
	old_att = models.IntegerField(default = 0)
	old_def = models.IntegerField(default = 0)
	banned = models.BooleanField(default = False)
	last_village = models.ForeignKey(Village, related_name = "last", null = True)
	is_active = models.BooleanField(default = False)
	activation_key = models.CharField(max_length = 25, null = True)
	profile = models.TextField(max_length = 1000, null = True)
	notes = models.TextField(max_length = 1000, null = True)
	parliament = models.BooleanField(default = False)
	in_ally = models.BooleanField(default = False)
	ne = 'ne'
	nw = 'nw'
	se = 'se'
	sw = 'sw'
	location_choices = (
		(ne, _('North East')),
		(nw , _('North West')),
		(se , _('South East')),
		(sw , _('South West')),
	)
	location = models.CharField(choices = location_choices, max_length = 5)
	next_update = models.DateTimeField(default = None, null = True)
	
def update_user_profile(sender, instance, created, **kwargs):
	if created:
		Player.objects.create(user=instance)
	instance.profile.save()
	
class Oasis(models.Model):
	location_latitude = models.IntegerField() # Because every oasis need co-ordinates
	location_longitude = models.IntegerField() # And two of them
	bonus_1 = models.IntegerField() # First bonus
	bonus_2 = models.IntegerField(null = True) # And possibly the seconday one
	army = models.ManyToManyField(Army)
	owner = models.ForeignKey(Player, null = True)
		
class Message(models.Model):
	sender = models.ForeignKey(Player, related_name="Sender")
	recipent = models.ForeignKey(Player, related_name="Recipent")
	content = models.TextField(max_length = 10**10)
	subject = models.CharField(max_length = 255)
	read = models.BooleanField(default = False)
	timestamp = models.DateTimeField(default = settings.START)
	
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
	name = models.CharField(default = "ABC", unique = True, max_length = 26)
	short_name = models.CharField(default="ABC", max_length = 6)
	
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
	def __unicode__(self):
		return unicode(self.typ)
	
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
	
