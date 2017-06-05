# -*- coding: utf-8 -*-

from models import *
from random import randint
import csv
from slugify import slugify
import building.models 
from datetime import time
from django.conf import settings

def village_init():
	a = [4,4,4,6] # 1 - 10
	b = [3,4,5,6] # 2 - 5
	c = [3,4,4,7] # 3 - 3
	d = [3,5,4,6] # 4 - 5
	e = [4,3,5,6] # 5 - 5 
	f = [4,5,3,6] # 6 - 5
	g = [4,4,3,7] # 7 - 3
	h = [4,3,4,7] # 8 - 3
	i = [3,3,3,9] # 9 - 2 
	j = [1,1,1,15] # 10 - 1
	mat = [a,b,c,d,e,f,g,h,i,j]
	for typ in mat:
		village = VillageType()
		village.oil_field = typ[0]
		village.forrest = typ[1]
		village.iron_mine = typ[2]
		village.farm = typ[3]
		village.save()
		
def tribe_init():
	partisan = 'Partisans'
	russian = 'Russians'
	american = 'Americans' 
	brits = 'Brittish' 
	german = 'Germans' 
	japs = 'Japanese'
	Tribe.objects.create(name = partisan)
	Tribe.objects.create(name = russian)
	Tribe.objects.create(name = american)
	Tribe.objects.create(name = brits)
	Tribe.objects.create(name = german)
	Tribe.objects.create(name = japs)
	
def map_init():
	village_init()
	for i in range (-10,11):
		print(i)
		for j in range (-10, 11):
			num = randint(1,20)
			if num < 14:
				typ = randint(1,55)
				village = Village()
				
				if typ < 11:
					village.typ = VillageType.objects.get(id = 1)
				elif typ < 16:
					village.typ = VillageType.objects.get(id = 2)
				elif typ < 21:
					village.typ = VillageType.objects.get(id = 4)
				elif typ < 26:
					village.typ = VillageType.objects.get(id = 5)
				elif typ < 31:
					village.typ = VillageType.objects.get(id = 6)
				elif typ < 34:
					village.typ = VillageType.objects.get(id = 3)
				elif typ < 37:
					village.typ = VillageType.objects.get(id = 7)
				elif typ < 40:
					village.typ = VillageType.objects.get(id = 8)
				elif typ < 42:
					village.typ = VillageType.objects.get(id = 9)
				else:
					village.typ = VillageType.objects.get(id = 10)
				village.location_latitude = i
				village.location_longitude = j
				village.save()
				continue
			if num < 19:
				bonuses = randint(1,4)
				oasiss = Oasis()
				oasiss.location_latitude = i
				oasiss.location_longitude = j
				oasiss.bonus_1 = randint(1,4)
				if bonuses == 1:
					oasiss.bonus_2 = 4
				oasiss.save()
				oasis = Oasis.objects.get(id = oasiss.id)
				army = Army()
				troops = Troops()
				troops.count = randint(0,50)
				troops.save()
				army.t0 = Troops.objects.get(id = troops.id)
				troops = Troops()
				troops.count = randint(0,45)
				troops.save()
				army.t1 = Troops.objects.get(id = troops.id)
				troops = Troops()
				troops.count = randint(0,40)
				troops.save()
				army.t2 = Troops.objects.get(id = troops.id)
				troops = Troops()
				troops.count = randint(0,40)
				troops.save()
				army.t3 = Troops.objects.get(id = troops.id)
				troops = Troops()
				troops.count = randint(0,35)
				troops.save()
				army.t4 = Troops.objects.get(id = troops.id)
				troops = Troops()
				troops.count = randint(0,30)
				troops.save()
				army.t5 = Troops.objects.get(id = troops.id)
				troops = Troops()
				troops.count = randint(0,30)
				troops.save()
				army.t6 = Troops.objects.get(id = troops.id)
				troops = Troops()
				troops.count = randint(0,25)
				troops.save()
				army.t7 = Troops.objects.get(id = troops.id)
				troops = Troops()
				troops.count = randint(0,20)
				troops.save()
				army.t8 = Troops.objects.get(id = troops.id)
				troops = Troops()
				troops.count = randint(0,20)
				troops.save()
				army.t9 = Troops.objects.get(id = troops.id)
				troops = Troops()
				troops.count = randint(0,15)
				troops.save()
				army.t10 = Troops.objects.get(id = troops.id)
				troops = Troops()
				troops.count = randint(0,10)
				troops.save()
				army.t11 = Troops.objects.get(id = troops.id)
				troops = Troops()
				troops.count = randint(0,5)
				troops.save()
				army.t12 = Troops.objects.get(id = troops.id)
				troops = Troops()
				troops.count = randint(0,5)
				troops.save()
				army.t13 = Troops.objects.get(id = troops.id)
				army.hero = False
				army.save()
				oasis.army.add(Army.objects.get(id = army.id))
				oasis.save()
				continue

def myround(x):
    return int(5 * round(float(x)/5))
				
def fields_init():
	fields = ['Oil field','Forrest','Iron mine','Farm']
	for item in fields:
		field = building.models.Field()
		field.name = str(item)
		try:
			field.image = 'init/img/fields/'+slugify(build)+'.png'
		except Exception:
			pass
		try:
			field.description = 'init/descriptions/fields/'+slugify(build)+'.txt'
		except Exception:
			pass
		field.save()
		print('init/'+slugify(str(field))+'.csv')
		with open('init/'+slugify(str(field))+'.csv', 'rb') as fin:
			spamreader = csv.reader(fin, delimiter=' ', quotechar='|')
			for lvl in spamreader:
				row = lvl[0].split(',')
				price = building.models.Cost()
				row[9] = float(row[9])
				price.days = row[9]//(3600*24)
				price.time = time(int(row[9]/3600)%24, int((row[9]%3600)/60), int((row[9]%60)), 0)
				price.oil = myround(row[2])
				price.iron = myround(row[3])
				price.wood = myround(row[4])
				price.food = myround(row[5])
				price.cost = int(row[6])
				price.culture_points = int(row[7])
				price.bonus = row[8]
				price.level = int(row[0])
				price.save()
				field.cost.add(price)
		field.save()
	return 0
	
def buildings_init():
	buildings = ['Parliament','Summer residence' ,'Town hall' ,'Headquarters' ,'Shelter' ,'Warehouse' ,'Silo' ,'University','Market','Training camp','Ammunition workshop' ,'Hangar','Railway' ,'Port' ,'Artilery mansion' ,"Hero's birth house",'Hideout' ,'Large warehouse','Large silo','Large camp','Large hangar','Bunker','Defensive line','Oil refinery','Iron works','Sawmill' ,'Slaughter house' ,'Can filling centre','Nuke research lab','Bazar']
	for build in buildings:
		bui = building.models.Building()
		bui.name = str(build)
		try:
			bui.image = 'init/img/buildings/'+slugify(build)+'.png'
		except Exception:
			pass
		try:
			bui.description = 'init/descriptions/buildings/'+slugify(build)+'.txt'
		except Exception:
			pass
		bui.save()
		print('init/'+slugify(str(build))+'.csv')
		with open('init/'+slugify(str(build))+'.csv', 'rb') as fin:
			spamreader = csv.reader(fin, delimiter=' ', quotechar='|')
			for lvl in spamreader:
				row = lvl[0].split(',')
				price = building.models.Cost()
				row[9] = float(row[9])
				price.days = row[9]//(3600*24)
				price.time = time(int(row[9]/3600)%24, int((row[9]%3600)/60), int((row[9]%60)), 0)
				price.oil = myround(row[2])
				price.iron = myround(row[3])
				price.wood = myround(row[4])
				price.food = myround(row[5])
				price.cost = int(row[6])
				price.culture_points = int(row[7])
				price.bonus = row[8]
				price.level = int(row[0])
				price.save()
				bui.cost.add(price)
		bui.save()
	return 0

