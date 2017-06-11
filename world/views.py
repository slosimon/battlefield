# -*- coding: utf-8 -*-
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_text
from django.template.loader import render_to_string
from world.forms import SignUpForm
from world.tokens import account_activation_token
from forms import *
from django.contrib.auth import authenticate, login
from models import *
import json
import urllib
import urllib2
from django.contrib import messages
from django.conf import settings
from world.initialize_model import map_init, tribe_init, buildings_init, fields_init
from world.functions import *
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime, timedelta
import operator
from django.contrib.auth.decorators import login_required
from update import *
from django.views.generic.list import ListView
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.timezone import utc
import get_buildings
from slugify import slugify

@login_required
def fields(request):
	user = request.user
	player = Player.objects.get(user = user)
	village_name = player.last_village.name
	update_res(player.last_village)
	resources = player.last_village.resources
	warehouse = player.last_village.storage_capacity
	silo = player.last_village.food_capacity
	fields = ['pos_01', 'pos_02', 'pos_03', 'pos_04', 'pos_05', 'pos_06', 'pos_07', 'pos_08', 'pos_09', 'pos_10', 'pos_11', 'pos_12', 'pos_13', 'pos_14', 'pos_15', 'pos_16', 'pos_17', 'pos_18']
	picture = []
	lvl = []
	name = []
	polja = player.last_village.fields
	for field in fields:
		polje = getattr(polja,field)
		name.append(polje.name.name)
		lvl.append(polje.lvl)
		try:
			picture.append(polje.name.image.url)
		except Exception:
			picture.append('/media/init/img/buildings/none.png')
	field = zip(fields,name,lvl,picture)
	oil = int(float(resources.oil) / warehouse * 100)
	iron = int(float(resources.iron) / warehouse * 100)
	wood = int(float(resources.wood) / warehouse * 100)
	food = int(float(resources.food) / silo * 100)
	production = player.last_village.production
	queue_name = []
	queue_end = []
	if player.last_village.field_1 is not None:
		queue_name.append(player.last_village.field_1.field.name.name)
		queue_end.append(player.last_village.field_1.end)
	if player.last_village.building_1 is not None:
		queue_name.append(player.last_village.building_1.building.building.name)
		queue_end.append(player.last_village.building_1.end)
	if player.last_village.field_2 is not None:
		queue_name.append(player.last_village.field_2.field.name.name)
		queue_end.append(player.last_village.field_2.end)
	if player.last_village.building_2 is not None:
		queue_name.append(player.last_village.building_2.building.building.name)
		queue_end.append(player.last_village.building_2.end)
	queue = zip(queue_name, queue_end)	
	return render(request, 'game/fields.html', {'player': player, 'village_name' : village_name, 'resources': resources, 'warehouse': warehouse, 'silo' : silo,'field':field, 'oil': oil, 'iron':iron, 'wood':wood, 'food':food, 'production':production, 'queue':queue})
	
@login_required	
def center(request):
	user = request.user
	player = Player.objects.get(user = user)
	update_res(player.last_village)
	village_name = player.last_village.name
	resources = player.last_village.resources
	warehouse = player.last_village.storage_capacity
	silo = player.last_village.food_capacity
	buildings = ['pos_01', 'pos_02', 'pos_03', 'pos_04', 'pos_05', 'pos_06', 'pos_07', 'pos_08', 'pos_09', 'pos_10', 'pos_11', 'pos_12', 'pos_13', 'pos_14', 'pos_15', 'pos_16', 'pos_17', 'pos_18', 'pos_19', 'pos_20', 'pos_21', 'pos_22', 'pos_23', 'pos_24']
	picture = []
	lvl = []
	name = [] 
	bajte = player.last_village.center
	for building in buildings:
		bajta = getattr(bajte, building)
		try:
			name.append(bajta.building.name)
			lvl.append(bajta.lvl)
		except Exception:
			name.append(_('Empty building spot'))
			lvl.append(0)
		try:
			picture.append(bajta.building.image.url)
		except Exception:
			picture.append('/media/init/img/buildings/none.png')
	field = zip(buildings,name,lvl,picture)
	oil = int(float(resources.oil) / warehouse * 100)
	iron = int(float(resources.iron) / warehouse * 100)
	wood = int(float(resources.wood) / warehouse * 100)
	food = int(float(resources.food) / silo * 100)
	production = player.last_village.production
	queue_name = []
	queue_end = []
	if player.last_village.field_1 is not None:
		queue_name.append(player.last_village.field_1.field.name.name)
		queue_end.append(player.last_village.field_1.end)
	if player.last_village.building_1 is not None:
		queue_name.append(player.last_village.building_1.building.building.name)
		queue_end.append(player.last_village.building_1.end)
	if player.last_village.field_2 is not None:
		queue_name.append(player.last_village.field_2.field.name.name)
		queue_end.append(player.last_village.field_2.end)
	if player.last_village.building_2 is not None:
		queue_name.append(player.last_village.building_2.building.building.name)
		queue_end.append(player.last_village.building_2.end)
	queue = zip(queue_name, queue_end)	
	return render(request, 'game/center.html', {'player': player, 'village_name' : village_name, 'resources': resources, 'warehouse': warehouse, 'silo' : silo,'field':field, 'oil': oil, 'iron':iron, 'wood':wood, 'food':food, 'production':production, 'queue':queue})
 
@login_required	
def pop_ranking(request):
	players = Player.objects.all().order_by('-population')
	count = Player.objects.count()
	bar = ['Player', 'Villages','Tribe','Population']
	if count > 20:
		paginator = Paginator(players, 20)
		i = 0
		while players[i].user.username != request.user.username:
			i += 1
		page = request.GET.get('page')
		try:
			users = paginator.page(page)
		except PageNotAnInteger:
			users = paginator.page((i+1)//20)
		except EmptyPage:
			users = paginator.page(paginator.num_pages)
			
		return render(request, 'game/ranking.html', {'users':users, 'bar':bar})
	else:
		return render(request, 'game/ranking.html', {'users':players, 'bar':bar})
		
@login_required	
def attack_ranking(request):
	players = Player.objects.all().order_by('-attack_points')
	count = Player.objects.count()
	bar = ['Player', 'Villages','Tribe','Attack Points']
	if count > 20:
		paginator = Paginator(players, 20)
		i = 0
		while players[i].user.username != request.user.username:
			i += 1
		page = request.GET.get('page')
		try:
			users = paginator.page(page)
		except PageNotAnInteger:
			users = paginator.page((i+1)//20)
		except EmptyPage:
			users = paginator.page(paginator.num_pages)
			
		return render(request, 'game/ranking_attack.html', {'users':users, 'bar':bar})
	else:
		return render(request, 'game/ranking_attack.html', {'users':players, 'bar':bar})
	
@login_required	
def def_ranking(request):
	players = Player.objects.all().order_by('-def_points')
	count = Player.objects.count()
	bar = ['Player', 'Villages','Tribe','Defense Points']
	if count > 20:
		paginator = Paginator(players, 20)
		i = 0
		while players[i].user.username != request.user.username:
			i += 1
		page = request.GET.get('page')
		try:
			users = paginator.page(page)
		except PageNotAnInteger:
			users = paginator.page((i+1)//20)
		except EmptyPage:
			users = paginator.page(paginator.num_pages)
			
		return render(request, 'game/ranking_def.html', {'users':users, 'bar':bar})
	else:
		return render(request, 'game/ranking_def.html', {'users':players, 'bar':bar})
	
@login_required	
def weekly_ranking(request):
	attack = Player.objects.extra(select={'offset': 'attack_points - old_att'}).order_by('-offset')
	defo = Player.objects.extra(select={'offset': 'def_points - old_def'}).order_by('-offset')
	rank = Player.objects.extra(select={'offset': 'population - old_rank'}).order_by('-offset')
	raid = Player.objects.all().order_by('-raided')
	user = request.user
	user = Player.objects.get(user = user)
	one = zip(attack,defo)
	two = zip(rank,raid)
	return render(request, 'game/ranking_weekly.html', {'user':user, 'one':one, 'two':two})
	
def find_headquarters_bonus(village):
	pos = ['pos_01','pos_02','pos_03','pos_04','pos_05','pos_06','pos_07','pos_08','pos_09','pos_10','pos_11','pos_12','pos_13','pos_14','pos_15','pos_16','pos_17','pos_18','pos_19','pos_20','pos_21','pos_22','pos_23','pos_24']
	for i in pos:
		path = getattr(village.center,i)
		if path.building.name == 'Headquarters':
			head = path.building.cost.filter(level = path.lvl)
			return head[0].bonus
			break
	return 100
			
@login_required
def field(request, pos):
	user = request.user
	player = Player.objects.get(user = user)
	village_name = player.last_village.name
	update_res(player.last_village)
	resources = player.last_village.resources
	warehouse = player.last_village.storage_capacity
	silo = player.last_village.food_capacity
	oil = int(float(resources.oil) / warehouse * 100)
	iron = int(float(resources.iron) / warehouse * 100)
	wood = int(float(resources.wood) / warehouse * 100)
	food = int(float(resources.food) / silo * 100)
	production = player.last_village.production
	field = getattr(player.last_village.fields, pos)
	current_lvl = field.lvl
	if player.last_village.field_1 is not None:
		if player.last_village.field_1.field == field:
			current_lvl += 1
	now = field.name.cost.filter(level = current_lvl)
	now = now[0]
	current_production = now.bonus
	nex = field.name.cost.filter(level = current_lvl+1)
	nex = nex[0]
	upgraded_production = nex.bonus
	cost_oil = nex.oil
	cost_iron = nex.iron
	cost_wood = nex.wood
	cost_food = nex.food
	needed = 0
	if field.name is not 'Farm':
		needed = nex.cost
	seconds = int(nex.time.second) + int(nex.time.minute)*60 + int(nex.time.hour)*3600 + int(nex.days) * 3600*24
	seconds = int(seconds * find_headquarters_bonus(player.last_village)/100)
	upgrade_time = str(str(int(seconds/3600)%24)+':'+ str(int((seconds%3600)/60)).zfill(2)+':'+str(int((seconds%60))).zfill(2))
	description = field.name.description
	ok = "0" # TODO
	if resources.oil >= cost_oil and resources.iron >= cost_iron and resources.wood >= cost_wood and resources.food >= cost_food and player.last_village.free_crop >= needed + 1:
		if player.last_village.field_1 is None:
			ok = "1"
		elif player.last_village.field_2 is None and player.bonuses.plus_account >= datetime.utcnow().replace(tzinfo=utc):
			ok = "1"
	try:
		picture = (field.name.image.url)
	except Exception:
		picture = ('/media/init/img/buildings/none.png')

	return render(request, 'game/field.html', {'player': player, 'village_name' : village_name, 'resources': resources, 'warehouse': warehouse, 'silo' : silo,'field':field, 'oil': oil, 'iron':iron, 'wood':wood, 'food':food, 'production':production, 'cost_oil':cost_oil, 'cost_iron':cost_iron, 'cost_wood': cost_wood, 'cost_food':cost_food, 'upgrade_time':upgrade_time, 'description':description, 'picture':picture, 'pos':pos, 'ok':ok, 'current_production':current_production, 'upgraded_production':upgraded_production})
	
def upgrade_field(request, pos):
	user = request.user
	player = Player.objects.get(user = user)
	update_res(player.last_village)
	resources = player.last_village.resources
	field = getattr(player.last_village.fields, pos)
	current_lvl = field.lvl
	nex = field.name.cost.filter(level = current_lvl+1)
	nex = nex[0]
	cost_oil = nex.oil
	cost_iron = nex.iron
	cost_wood = nex.wood
	cost_food = nex.food
	needed = 0
	if field.name is not 'Farm':
		needed = nex.cost
	seconds = int(nex.time.second) + int(nex.time.minute)*60 + int(nex.time.hour)*3600 + int(nex.days) * 3600*24
	seconds = int(seconds * find_headquarters_bonus(player.last_village)/100)
	upgrade_time = str(str(int(seconds/3600)%24)+':'+ str(int((seconds%3600)/60)).zfill(2)+':'+str(int((seconds%60))).zfill(2))
	if resources.oil >= cost_oil and resources.iron >= cost_iron and resources.wood >= cost_wood and resources.food >= cost_food and player.last_village.free_crop >= needed + 1:
		if player.last_village.field_1 is None:
			resources.oil -= cost_oil
			resources.iron -= cost_iron
			resources.wood -= cost_wood
			resources.food -= cost_food
			resources.save()
			queue = FieldQueue()
			queue.field = field
			queue.to = current_lvl+1
			queue.end = datetime.utcnow().replace(tzinfo=utc)+timedelta(seconds = seconds)
			queue.save()
			player.last_village.field_1 = queue
			player.last_village.next_update = queue.end
			player.last_village.save()
			player.next_update = queue.end
			player.save()
		elif player.last_village.field_2 is None and player.bonuses.plus_account >= datetime.utcnow().replace(tzinfo=utc):
			resources.oil -= cost_oil
			resources.iron -= cost_iron
			resources.wood -= cost_wood
			resources.food -= cost_food
			resources.save()
			queue = FieldQueue()
			queue.field = field
			queue.to = current_lvl+1
			queue.begin = player.last_village.field_1.end
			queue.end = player.last_village.field_1.end+timedelta(seconds = seconds)
			queue.save()
			player.last_village.field_2 = queue
			player.last_village.save()
	return redirect ('/fields/')
	
@login_required
def get_building(request, pos):
	user = request.user
	player = Player.objects.get(user = user)
	village_name = player.last_village.name
	update_res(player.last_village)
	resources = player.last_village.resources
	warehouse = player.last_village.storage_capacity
	silo = player.last_village.food_capacity
	oil = int(float(resources.oil) / warehouse * 100)
	iron = int(float(resources.iron) / warehouse * 100)
	wood = int(float(resources.wood) / warehouse * 100)
	food = int(float(resources.food) / silo * 100)
	production = player.last_village.production
	buildinga = getattr(player.last_village.center, pos)
	if buildinga is not None:
		current_lvl = buildinga.lvl
		if player.last_village.building_1 is not None:
			if player.last_village.building_1.building == buildinga:
				current_lvl += 1
		now = buildinga.building.cost.filter(level = current_lvl)
		now = now[0]
		current_production = now.bonus
		nex = buildinga.building.cost.filter(level = current_lvl+1)
		nex = nex[0]
		upgraded_production = nex.bonus
		cost_oil = nex.oil
		cost_iron = nex.iron
		cost_wood = nex.wood
		cost_food = nex.food
		seconds = int(nex.time.second) + int(nex.time.minute)*60 + int(nex.time.hour)*3600 + int(nex.days) * 3600*24
		seconds = int(seconds * find_headquarters_bonus(player.last_village)/100)
		upgrade_time = str(str(int(seconds/3600)%24)+':'+ str(int((seconds%3600)/60)).zfill(2)+':'+str(int((seconds%60))).zfill(2))
		description = buildinga.building.description
		ok = "0" # TODO
		if resources.oil >= cost_oil and resources.iron >= cost_iron and resources.wood >= cost_wood and resources.food >= cost_food and player.last_village.free_crop >= nex.cost + 1:
			if player.last_village.building_1 is None:
				ok = "1"
			elif player.last_village.building_2 is None and player.bonuses.plus_account >= datetime.utcnow().replace(tzinfo=utc):
				ok = "1"
		try:
			picture = (buildinga.building.image.url)
		except Exception:
			picture = ('/media/init/img/buildings/none.png')
		return render(request, 'game/building.html', {'player': player, 'village_name' : village_name, 'resources': resources, 'warehouse': warehouse, 'silo' : silo,'field':field, 'oil': oil, 'iron':iron, 'wood':wood, 'food':food, 'production':production, 'cost_oil':cost_oil, 'cost_iron':cost_iron, 'cost_wood': cost_wood, 'cost_food':cost_food, 'upgrade_time':upgrade_time, 'description':description, 'picture':picture, 'pos':pos, 'ok':ok})
	else:
		possible = get_buildings.get_possible(player)
		costa = []
		images = []
		description = []
		ok = []
		costs = building.models.Building.objects.all()
		for mozne in possible:
			for cena in costs:
				if cena.name == mozne:
					cost = cena.cost.filter(level = 1)
					cost = cost[0]
					costa.append(cost)
					try:
						images.append(cena.image)
					except Exception:
						images.append('/media/init/img/buildings/none.png')
					description.append(cena.description)
					tmp = "0" # TODO
					print(player.last_village.free_crop, cost.cost +1) 
					if resources.oil >= cost.oil and resources.iron >= cost.iron and resources.wood >= cost.wood and resources.food >= cost.food and player.last_village.free_crop >= cost.cost +1:
						if player.last_village.building_1 is None:
							tmp = "1"
						elif player.last_village.building_2 is None and player.bonuses.plus_account >= datetime.utcnow().replace(tzinfo=utc):
							tmp = "1"
					ok.append(tmp)
		mozne = zip(possible,costa, images, description, ok)
		return render(request, 'game/new-building.html', {'player': player, 'village_name' : village_name, 'resources': resources, 'warehouse': warehouse, 'silo' : silo, 'mozne':mozne, 'pos':pos, 'oil': oil, 'iron':iron, 'wood':wood, 'food':food, 'production':production,})
			
def upgrade_building(request, pos):
	user = request.user
	player = Player.objects.get(user = user)
	update_res(player.last_village)
	resources = player.last_village.resources
	building = getattr(player.last_village.center, pos)
	current_lvl = building.lvl
	nex = building.building.cost.filter(level = current_lvl+1)
	nex = nex[0]
	cost_oil = nex.oil
	cost_iron = nex.iron
	cost_wood = nex.wood
	cost_food = nex.food
	seconds = int(nex.time.second) + int(nex.time.minute)*60 + int(nex.time.hour)*3600 + int(nex.days) * 3600*24
	seconds = int(seconds * find_headquarters_bonus(player.last_village)/100)
	upgrade_time = str(str(int(seconds/3600)%24)+':'+ str(int((seconds%3600)/60)).zfill(2)+':'+str(int((seconds%60))).zfill(2))
	if resources.oil >= cost_oil and resources.iron >= cost_iron and resources.wood >= cost_wood and resources.food >= cost_food and player.last_village.free_crop >= nex.cost + 1:
		if player.last_village.building_1 is None:
			resources.oil -= cost_oil
			resources.iron -= cost_iron
			resources.wood -= cost_wood
			resources.food -= cost_food
			resources.save()
			queue = BuildingQueue()
			queue.building = building
			queue.to = current_lvl+1
			queue.end = datetime.utcnow().replace(tzinfo=utc)+timedelta(seconds = seconds)
			queue.save()
			player.last_village.building_1 = queue
			player.last_village.next_update = queue.end
			player.last_village.save()
			player.next_update = queue.end
			player.save()
		elif player.last_village.building_2 is None and player.bonuses.plus_account >= datetime.utcnow().replace(tzinfo=utc):
			resources.oil -= cost_oil
			resources.iron -= cost_iron
			resources.wood -= cost_wood
			resources.food -= cost_food
			resources.save()
			queue = BuildingQueue()
			queue.building = building
			queue.to = current_lvl+1
			queue.begin = player.last_village.building_1.end
			queue.end = player.last_village.building_1.end+timedelta(seconds = seconds)
			queue.save()
			player.last_village.building_2 = queue
			player.last_village.save()
	return redirect ('/center/')
	
def build(request,pos,bui):
	user = request.user
	player = Player.objects.get(user = user)
	
	village_name = player.last_village.name
	update_res(player.last_village)
	resources = player.last_village.resources
	warehouse = player.last_village.storage_capacity
	silo = player.last_village.food_capacity
	oil = int(float(resources.oil) / warehouse * 100)
	iron = int(float(resources.iron) / warehouse * 100)
	wood = int(float(resources.wood) / warehouse * 100)
	food = int(float(resources.food) / silo * 100)
	production = player.last_village.production
	buildings = building.models.Building.objects.all()
	buildinga = Building()
	for bajta in buildings:
		if slugify(bajta.name) == bui:
			buildinga.building = bajta
			buildinga.lvl = 0
	buildinga.save()
	cena = building.models.Building.objects.filter(name = buildinga.building)
	cena = cena[0].cost.filter(level = 1)
	cena = cena[0]
	if resources.oil >= cena.oil and resources.iron >= cena.iron and resources.wood >= cena.wood and resources.food >= cena.food and player.last_village.free_crop >= cena.cost + 1:
		setattr(player.last_village.center, pos, buildinga)
		player.last_village.center.save()
		upgrade_building(request, pos)
		return redirect('/center')
	else:
		# TODO Remove building
		return redirect('/center')
		
def maps(request,x,y):
	x = int(x)
	y = int(y)
	xcoords = []
	ycoords = []
	for i in range (7):
		if i+x-3 < -settings.MAP_SIZE:
			xcoords.append(settings.MAP_SIZE-(-i-x+2)%settings.MAP_SIZE)
		elif i+x-3 > settings.MAP_SIZE:
			xcoords.append(- 2 * settings.MAP_SIZE +i +x -4)
		else:
			xcoords.append(i+x-3)
		if i+y-3 < -settings.MAP_SIZE:
			ycoords.append(settings.MAP_SIZE-(-i-y+2)%settings.MAP_SIZE)
		elif i+y-3 > settings.MAP_SIZE:
			ycoords.append(- 2 * settings.MAP_SIZE +i +y -4)
		else:
			ycoords.append(i+y-3)
		print(xcoords,ycoords)
	ycoords = ycoords[::-1]
	village = []
	image = []
	ok = []
	for i in range(7):
		for j in range (7):
			try:
				selo = Village.objects.filter(location_latitude = xcoords[j], location_longitude = ycoords[i])[0]
				village.append(selo)
				if selo.population > 0:
					image.append('/media/villages/village.png')
				else:
					image.append('/media/villages/empty-village.png')
				ok.append(1)
			except Exception:
				try:
					selo = Oasis.objects.filter(location_latitude = xcoords[j], location_longitude = ycoords[i])[0]
					village.append(selo)
					image.append('/media/villages/oasis.png')
					ok.append(1)
				except:
					ok.append(0)
					village.append(0)
					image.append('/media/villages/empty.png')
	villages = zip(village,image,ok)
	return render(request, 'game/map.html', {'villages':villages})
			
	
	
	
