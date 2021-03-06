# -*- coding: utf-8 -*-

import datetime
from django.utils.timezone import utc
from django.conf import settings
import building
from models import *
from time import sleep
from datetime import timedelta
def update_real(village):
	village.real_production.oil = village.production.oil * (100.0+ village.bonus.oil)/100
	village.real_production.iron = village.production.iron * (100.0+ village.bonus.iron)/100
	village.real_production.wood = village.production.wood * (100.0+ village.bonus.wood)/100
	village.real_production.food = village.free_crop * (100.0+ village.bonus.food)/100
	village.real_production.save()
	village.save()
	
def update_res(village):
	now = datetime.utcnow().replace(tzinfo=utc)
	time_delta = (now - village.update).total_seconds()
	update_real(village)
	income = village.real_production
	holding = village.resources
	warehouse = village.storage_capacity
	silo = village.food_capacity
	
	wood = min(holding.wood + income.wood * (time_delta /60/60), warehouse)
	iron = min(holding.iron + income.iron * (time_delta /60/60), warehouse)
	oil = min(holding.oil + income.oil * (time_delta /60/60), warehouse)
	food = min(holding.food + income.food * (time_delta /60/60), silo)
	now = datetime.utcnow().replace(tzinfo=utc)
	village.update = now
	village.resources.oil = oil
	village.resources.iron = iron
	village.resources.wood = wood
	village.resources.food = food
	village.resources.save()
	village.save()

def update_production(village, typ, lvl):
	field = typ
	field.lvl += 1
	field.save()
	typ = field.name.name
	update_res(village)
	if typ == 'Oil field':
		res = 'oil'
	elif typ == 'Iron mine':
		res = 'iron'
	elif typ == 'Forrest':
		res = 'wood'
	else:
		res = 'food'
	typ = field.name.cost
	get_bonus = typ.filter(level = lvl-1)
	get_new = typ.filter(level = lvl)
	village.free_crop -= get_new[0].cost
	village.production.food -= get_new[0].cost
	village.population += get_new[0].cost
	up = getattr(village.production,res)
	if res == 'food':
		village.free_crop += (int(get_new[0].bonus) - int(get_bonus[0].bonus))
	up = up + (int(get_new[0].bonus) - int(get_bonus[0].bonus))
	setattr(village.production, res, up)
	village.production.save()
	village.culture_points += get_new[0].culture_points
	village.save()
	update_res(village)
	update_real(village)
	
def update_building(village, typ, lvl):
	building = typ
	building.lvl += 1
	building.save()
	typ = building.building.cost
	get_new = typ.filter(level = lvl)
	if building.building.name == 'Warehouse':
		warehouse = building.building
		village.storage_capacity += (warehouse.cost.filter(level = lvl+1)[0].bonus - warehouse.cost.filter(level = lvl)[0].bonus)
	if building.building.name == 'Silo':
		warehouse = building.building
		village.food_capacity += (warehouse.cost.filter(level = lvl+1)[0].bonus - warehouse.cost.filter(level = lvl)[0].bonus)
	village.production.food -= get_new[0].cost
	village.population += get_new[0].cost
	village.free_crop -= get_new[0].cost
	village.production.save()
	village.culture_points += get_new[0].culture_points
	village.save()
	update_res(village)

def queue(): # TODO when army system
	sleep(2)
	while True:
		players = Player.objects.exclude(next_update__isnull = True).order_by('next_update')
		if len(players) > 0:
			villages = players[0].villages.exclude(next_update__isnull = True).order_by('next_update')
			
			if len(villages) > 0:
				if villages[0].field_1 is not None and villages[0].building_1 is not None:
					
					if villages[0].field_1.end <= villages[0].building_1.end and villages[0].field_1.end <= datetime.utcnow().replace(tzinfo=utc):
						update_production(villages[0], villages[0].field_1.field, villages[0].field_1.to)
						if villages[0].field_2 is not None:
							villages[0].field_1 = villages[0].field_2
							villages[0].field_1.save()
						else:
							villages[0].field_1 = None
						
						villages[0].field_2 = None
						if villages[0].field_1 is not None:
							villages[0].next_update = min(villages[0].field_1.end, villages[0].building_1.end)
						elif villages[0].building_1 is not None:
							villages[0].next_update = villages[0].building_1.end
						else:
							villages[0].next_update = None
						villages[0].save()
						players = []
						continue
					if villages[0].field_1.end > villages[0].building_1.end and villages[0].building_1.end <= datetime.utcnow().replace(tzinfo=utc):
						update_building(villages[0], villages[0].building_1.building, villages[0].building_1.to)
						if villages[0].building_2 is not None:
							villages[0].building_1 = villages[0].building_2
							villages[0].building_1.start = None
						else:
							villages[0].building_1 = None
						villages[0].building_2 = None
						if villages[0].building_1 is not None:
							villages[0].next_update = min(villages[0].building_1.end, villages[0].field_1.end)
						elif villages[0].field_1 is not None:
							villages[0].next_update = villages[0].field_1.end
						else:
							villages[0].next_update = None
						villages[0].save()
						players = []
						continue
					#if villages[0].building_1.end <= datetime.utcnow().replace(tzinfo=utc):
						
						#update_building(villages[0], villages[0].building_1.building, villages[0].building_1.to)
						#if villages[0].building_2 is not None:
							#villages[0].building_1 = villages[0].building_2
							#villages[0].building_1.start = None
						#else:
							#villages[0].building_1 = None
						#villages[0].building_2 = None
						#if villages[0].building_1 is not None:
							#villages[0].next_update = building_1.end
						#else:
							#villages[0].next_update = None
						#villages[0].save()
						#players = []
						
				elif villages[0].field_1 is not None:
					
					if villages[0].field_1.end <= datetime.utcnow().replace(tzinfo=utc):
						update_production(villages[0], villages[0].field_1.field, villages[0].field_1.to)
						if villages[0].field_2 is not None:
							villages[0].field_1 = villages[0].field_2
							villages[0].field_1.save()
						else:
							villages[0].field_1 = None
						
						villages[0].field_2 = None
						if villages[0].field_1 is not None:
							villages[0].next_update = villages[0].field_1.end
						else:
							villages[0].next_update = None
						villages[0].save()
						players = []
						
				elif villages[0].building_1 is not None:
					
					if villages[0].building_1.end <= datetime.utcnow().replace(tzinfo=utc):
						update_building(villages[0], villages[0].building_1.building, villages[0].building_1.to)
						if villages[0].building_2 is not None:
							villages[0].building_1 = villages[0].building_2
							villages[0].building_1.start = None
						else:
							villages[0].building_1 = None
						villages[0].building_2 = None
						if villages[0].building_1 is not None:
							villages[0].next_update = villages[0].building_1.end
						else:
							villages[0].next_update = None
						villages[0].save()
						players = []
			players = Player.objects.exclude(next_update__isnull = True).order_by('next_update')
			villages = players[0].villages.exclude(next_update__isnull = True).order_by('next_update')
			player = players[0]
			if len(villages) > 0:
				player.next_update = villages[0].next_update
			else:
				setattr(player, 'next_update', None)
				player.save()
				print(player.next_update)
			player.save()
		else:
			
			sleep(1)
			
def population():
	while True:
		players = Player.objects.all()
		for player in players:
			villages = player.villages.all()
			count = 0
			culture = 0
			for village in villages:
				count += village.population
				culture += village.culture_points
			player.population = count
			time = (datetime.utcnow().replace(tzinfo=utc) - player.last_update).total_seconds()*1.0/3600.0/24.0
			player.culture_points += (culture * time)
			player.last_update = datetime.utcnow().replace(tzinfo=utc)
			player.save()
		sleep(60)
		

