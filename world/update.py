# -*- coding: utf-8 -*-

import datetime
from django.utils.timezone import utc
from django.conf import settings
import building
from models import *

	
def update_res(village):
	now = datetime.utcnow().replace(tzinfo=utc)
	time_delta = (now - village.update).total_seconds()
	income = village.production
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
	get_bonus = typ.filter(level = lvl -1)
	get_new = typ.filter(level = lvl)
	village.production.food -= get_new[0].cost
	up = getattr(village.production,res)
	up += (getattr(get_new[0],res) - getattr(get_bonus[0],res))
	village.production.save()
	village.save()
	
def update_building(village, typ, lvl):
	building = getattr(village.center,typ)
	building.lvl += 1
	building.save()
	typ = building.building.name
	get_new = typ.objects.filter(level = lvl)
	village.production.food -= get_new[0]
	village.save()
	update_res(village)

def queue():
	while True:
		players = Player.objects.exclude(next_update__isnull = True).order_by('next_update')
		
		if len(players) > 0:
			villages = players[0].villages.exclude(next_update__isnull = True).order_by('next_update')
			
			if len(villages) > 0:
				if villages[0].field_1 is not None and villages[0].building_1 is not None:
					if villages[0].field_1.end <= villages[0].building_1.end and villages[0].field_1.end <= datetime.utcnow().replace(tzinfo=utc):
						update_production(villages[0], villages[0].field_1.field, villages[0].field_1.to)
						villages[0].field_1 = villages[0].field_2
						villages[0].field_1.start = None
						villages[0].field_1.save()
						villages[0].field_2 = None
						villages[0].field_2.save()
						print("Deleting ...")
						if villages[0].field_1 is not None:
							villages[0].next_update = villages[0].field_1.next_update
						else:
							villages[0].next_update = None
						villages[0].save()
					if villages[0].field_1.end >= villages[0].building_1.end:
						update_building(villages[0], villages[0].building_1.building, villages[0].building_1.to)
						villages[0].buiilding_1 = villages[0].building_2
						villages[0].building_1.start = None
						villages[0].building_1.save()
						villages[0].building_2 = None
						villages[0].building_2.save()
						if villages[0].building_1 is not None:
							villages[0].next_update = building_1.next_update
						else:
							villages[0].next_update = None
						villages[0].save()
				elif villages[0].field_1 is not None:
					if villages[0].field_1.end <= datetime.utcnow().replace(tzinfo=utc):
						update_production(villages[0], villages[0].field_1.field, villages[0].field_1.to)
						if villages[0].field_2 is not None:
							villages[0].field_1 = villages[0].field_2
							villages[0].field_1.save()
						else:
							villages[0].field_1 = None
						
						villages[0].field_2 = None
						print("Deleting ...")
						if villages[0].field_1 is not None:
							villages[0].next_update = villages[0].field_1.next_update
						else:
							villages[0].next_update = None
						villages[0].save()
				elif villages[0].building_1 is not None:
					if villages[0].building_1.end <= datetime.utcnow().replace(tzinfo=utc):
						update_building(villages[0], villages[0].building_1.building, villages[0].building_1.to)
						villages[0].buiilding_1 = villages[0].building_2
						villages[0].building_1.start = None
						villages[0].building_1.save()
						villages[0].building_2 = None
						villages[0].building_2.save()
						if villages[0].building_1 is not None:
							villages[0].next_update = building_1.next_update
						else:
							villages[0].next_update = None
						villages[0].save()

