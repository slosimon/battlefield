# -*- coding: utf-8 -*-

from models import *
import building
def village_start(village):
	buildings = building.Building().objects.get(name = 'Headquarters')
	build = Building()
	build.building = buildings
	building.save()
	center = Center()
	center.pos_01 = building
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
	field1 = Field.objects.create(name = building.Field.objects.get(name = fields[0]), lvl = 0)
	field2 = Field.objects.create(name = building.Field.objects.get(fields[1]), lvl = 0)
	field3 = Field.objects.create(name = building.Field.objects.get(fields[2]), lvl = 0)
	field4 = Field.objects.create(name = building.Field.objects.get(fields[3]), lvl = 0)
	field5 = Field.objects.create(name = building.Field.objects.get(fields[4]), lvl = 0)
	field6 = Field.objects.create(name = building.Field.objects.get(fields[5]), lvl = 0)
	field7 = Field.objects.create(name = building.Field.objects.get(fields[6]), lvl = 0)
	field8 = Field.objects.create(name = building.Field.objects.get(fields[7]), lvl = 0)
	field9 = Field.objects.create(name = building.Field.objects.get(fields[8]), lvl = 0)
	field10 = Field.objects.create(name = building.Field.objects.get(fields[9]), lvl = 0)
	field11 = Field.objects.create(name = building.Field.objects.get(fields[10]), lvl = 0)
	field12 = Field.objects.create(name = building.Field.objects.get(fields[11]), lvl = 0)
	field13 = Field.objects.create(name = building.Field.objects.get(fields[12]), lvl = 0)
	field14 = Field.objects.create(name = building.Field.objects.get(fields[13]), lvl = 0)
	field15 = Field.objects.create(name = building.Field.objects.get(fields[14]), lvl = 0)
	field16 = Field.objects.create(name = building.Field.objects.get(fields[15]), lvl = 0)
	field17 = Field.objects.create(name = building.Field.objects.get(fields[16]), lvl = 0)
	field18 = Field.objects.create(name = building.Field.objects.get(fields[17]), lvl = 0)
	fields = Fields.objects.create(pos_01 = field1, pos_02 = field2, pos_03 = field3, pos_04 = field4, pos_05 = field5, pos_06 = field6, pos_07 = field7, pos_08 = field8, pos_09 = field9, pos_10 = field10, pos_11 = field11, pos_12 = field12, pos_13 = field13, pos_14 = field14, pos_15 = field15, pos_16 = field16, pos_17 = field17, pos_18 = field18)
	army = Army()
	troops = Troops()
	troops.count = 0
	troops.save()
	army.t0 = Troops.objects.get(id = troops.id)
	troops = Troops()
	troops.count = 0
	troops.save()
	army.t1 = Troops.objects.get(id = troops.id)
	troops = Troops()
	troops.count = 0
	troops.save()
	army.t2 = Troops.objects.get(id = troops.id)
	troops = Troops()
	troops.count = 0
	troops.save()
	army.t3 = Troops.objects.get(id = troops.id)
	troops = Troops()
	troops.count = 0
	troops.save()
	army.t4 = Troops.objects.get(id = troops.id)
	troops = Troops()
	troops.count = 0
	troops.save()
	army.t5 = Troops.objects.get(id = troops.id)
	troops = Troops()
	troops.count = 0
	troops.save()
	army.t6 = Troops.objects.get(id = troops.id)
	troops = Troops()
	troops.count = 0
	troops.save()
	army.t7 = Troops.objects.get(id = troops.id)
	troops = Troops()
	troops.count = 0
	troops.save()
	army.t8 = Troops.objects.get(id = troops.id)
	troops = Troops()
	troops.count = 0
	troops.save()
	army.t9 = Troops.objects.get(id = troops.id)
	troops = Troops()
	troops.count = 0
	troops.save()
	army.t10 = Troops.objects.get(id = troops.id)
	troops = Troops()
	troops.count = 0
	troops.save()
	army.t11 = Troops.objects.get(id = troops.id)
	troops = Troops()
	troops.count = 0
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
	production = Resources.objects.create(oil = 10, iron = 10, wood = 10, food = 20)
	production.save()
	village.production = production
	village.save()
	return 0
