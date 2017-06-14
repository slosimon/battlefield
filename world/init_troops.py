# -*- coding: utf-8 -*-

from models import *
from random import randint
import csv
from slugify import slugify
import building.models 
import datetime
from django.conf import settings
import world

def init_types():
	l = ['Infantry', 'Aviation', 'Artillery', 'Navy']
	for i in l:
		troops.models.Troop_type.objects.create(typ = i)
		
def divide(tim):
	if tim == datetime.time(0,0):
		return datetime.time(0,0,0,0)
	else:
		seconds = 3600*int(tim.hour)+ 60* int(tim.minute)
		seconds = seconds // settings.SPEED
		return datetime.time(seconds //3600, (seconds % 3600) //60, seconds % 60, 0)

def myround(x):
    return int(5 * round(float(x)/5))
    
def initialize():
	tribes = ['Partisans','Russians','Americans','Brittish','Germans','Japanese']#,'Aliens']
	locations = ['partisans','russians','americans','brits','germans','japanese']#,'aliens']
	init_types()
	for i in range(len(locations)):
		with open('init/'+locations[i]+'/troops.csv', 'rb') as fin:
			spamreader = csv.reader(fin, delimiter=',', quotechar='|')
			j = 0
			lista = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13']
			if i == 0:
				army = Partisan_troops()
			if i == 1:
				army = Russian_troops()
			if i == 2:
				army = American_troops()
			if i == 3:
				army = Brittish_troops()
			if i == 4:
				army = German_troops()
			if i == 5:
				army = Japanese_troops()
			#if i == 6:
				#
			for lvl in spamreader:
				row = lvl
				length = len(row)
				research_cost = troops.models.Resources.objects.create(oil = row[17], iron = row[18], wood = row[19], food = row[20])
				training_cost = troops.models.Resources.objects.create(oil= row[4], iron = row[5], wood = row[6], food = row[7])
				troop_type = troops.models.Troop_type.objects.filter(typ = row[1])[0]
				research_time = divide(datetime.datetime.strptime(row[16], '%H:%M:%S').time())
				training_time = divide(datetime.datetime.strptime(row[3], '%H:%M:%S').time())
				description = slugify(row[0])
				a = troops.models.Troops.objects.create(research_time = research_time, research_cost = research_cost, training_cost = training_cost, training_time = training_time, image = 'init/img/troops/'+locations[i]+'/'+slugify(row[0])+'.png', description = description, name = row[0], consumption = row[8], attack_power = row[9], def_infantry = row[10], def_aviation = row[11], def_marine = row[12], def_artilery = row[13], troop_type = troop_type, carry = row[14], destruction_power = row[15], speed = row[2])
				if j < 13:
					for n in range (20):
						b = troops.models.UpgradeResources.objects.create(oil = myround(int(row[4]) * 3 * 1.13**n), iron = myround(int(row[5]) * 3 * 1.13**n), wood = myround(int(row[6]) * 3 * 1.13**n), food = myround((int(row[7]) * 3 * 1.13**n)), lvl = n+1)
						a.upgrade_cost.add(b)
				troop = Troop.objects.create(troop = a)
				setattr(army,lista[j],troop)
				j += 1
			army.save()
	
