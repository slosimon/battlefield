# -*- coding: utf-8 -*-

from models import *
from building.models import Building as Bbuilding
from building.models import Field as Bfield
from django.conf import settings
from django.utils.timezone import utc
from datetime import datetime

def village_start(player, village):
	buildings = Bbuilding.objects.get(name = 'Headquarters')
	build = Building()
	build.building = buildings
	build.lvl = 1
	build.save()
	center = Center() 
	center.pos_01 = build
	center.save()
	village.center = center
	fields = []
	for i in range (village.typ.oil_field):
		fields.append('Oil field')
	for i in range (village.typ.iron_mine):
		fields.append('Iron mine')
	for i in range (village.typ.forrest):
		fields.append('Forrest')
	for i in range (village.typ.farm):
		fields.append('Farm')
	
	field1 = Field.objects.create(name = Bfield.objects.get(name = fields[0]), lvl = 0)
	field2 = Field.objects.create(name = Bfield.objects.get(name = fields[1]), lvl = 0)
	field3 = Field.objects.create(name = Bfield.objects.get(name = fields[2]), lvl = 0)
	field4 = Field.objects.create(name = Bfield.objects.get(name = fields[3]), lvl = 0)
	field5 = Field.objects.create(name = Bfield.objects.get(name = fields[4]), lvl = 0)
	field6 = Field.objects.create(name = Bfield.objects.get(name = fields[5]), lvl = 0)
	field7 = Field.objects.create(name = Bfield.objects.get(name = fields[6]), lvl = 0)
	field8 = Field.objects.create(name = Bfield.objects.get(name = fields[7]), lvl = 0)
	field9 = Field.objects.create(name = Bfield.objects.get(name = fields[8]), lvl = 0)
	field10 = Field.objects.create(name = Bfield.objects.get(name = fields[9]), lvl = 0)
	field11 = Field.objects.create(name = Bfield.objects.get(name = fields[10]), lvl = 0)
	field12 = Field.objects.create(name = Bfield.objects.get(name = fields[11]), lvl = 0)
	field13 = Field.objects.create(name = Bfield.objects.get(name = fields[12]), lvl = 0)
	field14 = Field.objects.create(name = Bfield.objects.get(name = fields[13]), lvl = 0)
	field15 = Field.objects.create(name = Bfield.objects.get(name = fields[14]), lvl = 0)
	field16 = Field.objects.create(name = Bfield.objects.get(name = fields[15]), lvl = 0)
	field17 = Field.objects.create(name = Bfield.objects.get(name = fields[16]), lvl = 0)
	field18 = Field.objects.create(name = Bfield.objects.get(name = fields[17]), lvl = 0)
	a = Fields.objects.create(pos_01 = field1, pos_02 = field2, pos_03 = field3, pos_04 = field4, pos_05 = field5, pos_06 = field6, pos_07 = field7, pos_08 = field8, pos_09 = field9, pos_10 = field10, pos_11 = field11, pos_12 = field12, pos_13 = field13, pos_14 = field14, pos_15 = field15, pos_16 = field16, pos_17 = field17, pos_18 = field18)
	village.fields = a
	army = Army()
	troops = Troops()
	troops.count = 0
	troops.save()
	army.t0 = Troops.objects.get(id = troops.id)
	troops = Troops()
	troops.count = -1
	troops.save()
	army.t1 = Troops.objects.get(id = troops.id)
	troops = Troops()
	troops.count = -1
	troops.save()
	army.t2 = Troops.objects.get(id = troops.id)
	troops = Troops()
	troops.count = -1
	troops.save()
	army.t3 = Troops.objects.get(id = troops.id)
	troops = Troops()
	troops.count = -1
	troops.save()
	army.t4 = Troops.objects.get(id = troops.id)
	troops = Troops()
	troops.count = -1
	troops.save()
	army.t5 = Troops.objects.get(id = troops.id)
	troops = Troops()
	troops.count = -1
	troops.save()
	army.t6 = Troops.objects.get(id = troops.id)
	troops = Troops()
	troops.count = -1
	troops.save()
	army.t7 = Troops.objects.get(id = troops.id)
	troops = Troops()
	troops.count = -1
	troops.save()
	army.t8 = Troops.objects.get(id = troops.id)
	troops = Troops()
	troops.count = -1
	troops.save()
	army.t9 = Troops.objects.get(id = troops.id)
	troops = Troops()
	troops.count = -1
	troops.save()
	army.t10 = Troops.objects.get(id = troops.id)
	troops = Troops()
	troops.count = -1
	troops.save()
	army.t11 = Troops.objects.get(id = troops.id)
	troops = Troops()
	troops.count = -1
	troops.save()
	army.t12 = Troops.objects.get(id = troops.id)
	troops = Troops()
	troops.count = 0
	troops.save()
	army.t13 = Troops.objects.get(id = troops.id)
	army.save()
	village.army = (army)
	resources = Resources()
	resources.save()
	village.resources = resources
	village.update = datetime.now()
	typ = village.typ
	production = Resources.objects.create(oil = 2 * typ.oil_field * settings.SPEED, iron = 2 * typ.oil_field * settings.SPEED, wood = 2 * typ.oil_field * settings.SPEED, food = 2 * typ.oil_field * settings.SPEED)
	production.save()
	real = Resources.objects.create(oil = 2 * typ.oil_field * settings.SPEED, iron = 2 * typ.oil_field * settings.SPEED, wood = 2 * typ.oil_field * settings.SPEED, food = 2 * typ.oil_field * settings.SPEED)
	real.save()
	village.real_production = real
	village.free_crop = real.food - 2
	if player.bonuses.oil_bonus_production > datetime.utcnow().replace(tzinfo=utc):
		oil = 25
	else:
		oil = 0
	if player.bonuses.iron_bonus_production > datetime.utcnow().replace(tzinfo=utc):
		iron = 25
	else:
		iron = 0
	if player.bonuses.wood_bonus_production > datetime.utcnow().replace(tzinfo=utc):
		wood = 25
	else:
		wood = 0
	if player.bonuses.food_bonus_production > datetime.utcnow().replace(tzinfo=utc):
		food = 25
	else:
		food = 0
		
	bonus = Resources.objects.create(oil = oil, iron = iron, wood = wood, food = food)
	bonus.save()
	village.bonus = bonus 
	village.production = production
	village.save()
	return 0
