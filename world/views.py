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
from math import floor
from slugify import slugify

def count_messages(request):
	player = Player.objects.get(user = request.user)
	return len(Message.objects.filter(read = False, recipent = player))

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
	production = player.last_village.real_production
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
	ok = False
	if len(queue_name) > 0 :
		if player.gold >= 2 or player.gold < 0 :
			ok = True	
	return render(request, 'game/fields.html', {'player': player, 'village_name' : village_name, 'resources': resources, 'warehouse': warehouse, 'silo' : silo,'field':field, 'oil': oil, 'iron':iron, 'wood':wood, 'food':food, 'production':production, 'queue':queue, 'player':player, 'unread_messages':count_messages(request), 'ok':ok})
	
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
	production = player.last_village.real_production
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
	ok = False
	if len(queue_name) > 0 :
		if player.gold >= 2 or player.gold < 0 :
			ok = True
	return render(request, 'game/center.html', {'player': player, 'village_name' : village_name, 'resources': resources, 'warehouse': warehouse, 'silo' : silo,'field':field, 'oil': oil, 'iron':iron, 'wood':wood, 'food':food, 'production':production, 'queue':queue, 'player':player, 'unread_messages':count_messages(request), 'ok':ok})
 
@login_required	
def pop_ranking(request):
	players = Player.objects.all().order_by('-population')
	count = Player.objects.count()
	player = Player.objects.get(user = request.user)
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
			
		return render(request, 'game/ranking.html', {'users':users, 'bar':bar, 'player':player, 'unread_messages':count_messages(request)})
	else:
		return render(request, 'game/ranking.html', {'users':players, 'bar':bar, 'player':player, 'unread_messages':count_messages(request)})
		
@login_required	
def attack_ranking(request):
	players = Player.objects.all().order_by('-attack_points')
	count = Player.objects.count()
	player = Player.objects.get(user = request.user)
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
			
		return render(request, 'game/ranking_attack.html', {'users':users, 'bar':bar, 'player':player, 'unread_messages':count_messages(request)})
	else:
		return render(request, 'game/ranking_attack.html', {'users':players, 'bar':bar, 'player':player, 'unread_messages':count_messages(request)})
	
@login_required	
def def_ranking(request):
	players = Player.objects.all().order_by('-def_points')
	count = Player.objects.count()
	player = Player.objects.get(user = request.user)
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
			
		return render(request, 'game/ranking_def.html', {'users':users, 'bar':bar, 'player':player, 'unread_messages':count_messages(request)})
	else:
		return render(request, 'game/ranking_def.html', {'users':players, 'bar':bar, 'player':player, 'unread_messages':count_messages(request)})
	
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
	player = Player.objects.get(user = request.user)
	return render(request, 'game/ranking_weekly.html', {'user':user, 'one':one, 'two':two, 'player':player, 'unread_messages':count_messages(request)})
	
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
	production = player.last_village.real_production
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
	if str(field.name) == str('Farm'):
		needed = -100000
	else:
		needed = nex.cost
	seconds = int(nex.time.second) + int(nex.time.minute)*60 + int(nex.time.hour)*3600 + int(nex.days) * 3600*24
	seconds = int(seconds * find_headquarters_bonus(player.last_village)/100)
	upgrade_time = str(str(int(seconds/3600)%24)+':'+ str(int((seconds%3600)/60)).zfill(2)+':'+str(int((seconds%60))).zfill(2))
	description = field.name.description
	ok = "0" # TODO
	if resources.oil >= cost_oil and resources.iron >= cost_iron and resources.wood >= cost_wood and resources.food >= cost_food and player.last_village.free_crop >= needed + 1 and (nex.level <= 10 or player.last_village.capital):
		if player.last_village.field_1 is None:
			ok = "1"
		elif player.last_village.field_2 is None and player.bonuses.plus_account >= datetime.utcnow().replace(tzinfo=utc):
			ok = "1"
	try:
		picture = (field.name.image.url)
	except Exception:
		picture = ('/media/init/img/buildings/none.png')

	return render(request, 'game/field.html', {'player': player, 'village_name' : village_name, 'resources': resources, 'warehouse': warehouse, 'silo' : silo,'field':field, 'oil': oil, 'iron':iron, 'wood':wood, 'food':food, 'production':production, 'cost_oil':cost_oil, 'cost_iron':cost_iron, 'cost_wood': cost_wood, 'cost_food':cost_food, 'upgrade_time':upgrade_time, 'description':description, 'picture':picture, 'pos':pos, 'ok':ok, 'current_production':current_production, 'upgraded_production':upgraded_production, 'unread_messages':count_messages(request)})
	
@login_required	
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
	if str(field.name) == str('Farm'):
		needed = -100000
	else:
		needed = nex.cost
	seconds = int(nex.time.second) + int(nex.time.minute)*60 + int(nex.time.hour)*3600 + int(nex.days) * 3600*24
	seconds = int(seconds * find_headquarters_bonus(player.last_village)/100)
	upgrade_time = str(str(int(seconds/3600)%24)+':'+ str(int((seconds%3600)/60)).zfill(2)+':'+str(int((seconds%60))).zfill(2))
	if resources.oil >= cost_oil and resources.iron >= cost_iron and resources.wood >= cost_wood and resources.food >= cost_food and player.last_village.free_crop >= needed + 1 and (nex.level <= 10 or player.last_village.capital): 
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
	production = player.last_village.real_production
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
			
		# TODO view based on building (market, bunker, hero's birth house, townhall, university (SUM = 5) )
		if buildinga.building.name == 'Training camp':
			form = CampForm(request.POST, player_id = player.id, lvl = buildinga.lvl)
			if request.method == 'POST':
				
				if form.is_valid():
					
					if player.tribe.name == 'Partisans':
						army = Partisan_troops.objects.get(id = 1)
					elif player.tribe.name == 'Russians':
						army = Russian_troops.objects.get(id = 1)
					elif player.tribe.name == 'Americans':
						army = American_troops.objects.get(id = 1)
					elif player.tribe.name == 'Brittish':
						army = Brittish_troops.objects.get(id = 1)
					elif player.tribe.name == 'Germans':
						army = German_troops.objects.get(id = 1)
					elif player.tribe.name == 'Japanese':
						army = Japanese_troops.objects.get(id = 1)
						
					if player.last_village.training_queue is not None:
						queue = player.last_village.training_queue
						if queue.barracks is not None:
							barracks = queue.barracks__set.order_by('-end_time')
							if barracks.end_time < datetime.utcnow().replace(tzinfo=utc):
								if form.cleaned_data.get('t0') > 0:
									nex = army.t0.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t0')), maximum)
									new = Queue(troop = army.t0, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t0.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
								elif form.cleaned_data.get('t1') > 0:
									nex = army.t1.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t1')), maximum)
									new = Queue(troop = army.t1, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t1.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
							else:
								if form.cleaned_data.get('t0') > 0:
									nex = army.t0.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t0')), maximum)
									new = Queue(troop = army.t0, quantity = int(train), start_time = barracks.end_time, end_time = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = barracks.end_time + timedelta(int( seconds = (int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = barracks.end_time, building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t0.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
								elif form.cleaned_data.get('t1') > 0:
									nex = army.t1.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t1')), maximum)
									new = Queue(troop = army.t1, quantity = int(train), start_time = barracks.end_time, end_time = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = barracks.end_time, building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t1.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
							new.save()
							queue.add(new)
							queue.save()
						else:
							if form.cleaned_data.get('t0') > 0:
								nex = army.t0.troop.training_time
								maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
								train = min(int(form.cleaned_data.get('t0')), maximum)
								new = Queue(troop = army.t0, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
								take = player.last_village.resources
								cost = army.t0.troop.training_cost
								take.oil -= cost.oil * train
								take.iron -= cost.iron * train
								take.wood -= cost.wood * train
								take.food -= cost.food * train
								take.save()
							elif form.cleaned_data.get('t1') > 0:
								nex = army.t1.troop.training_time
								maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
								train = min(int(form.cleaned_data.get('t1')), maximum)
								new = Queue(troop = army.t1, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
								take = player.last_village.resources
								cost = army.t1.troop.training_cost
								take.oil -= cost.oil * train
								take.iron -= cost.iron * train
								take.wood -= cost.wood * train
								take.food -= cost.food * train
								take.save()
							new.save()
							bar = Barracks()
							bar.save()
							bar.queue.add(new)
							bar.save()
					else:
						if form.cleaned_data.get('t0') > 0:
							nex = army.t0.troop.training_time
							maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
							train = min(int(form.cleaned_data.get('t0')), maximum)
							new = Queue(troop = army.t0, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
							take = player.last_village.resources
							cost = army.t0.troop.training_cost
							take.oil -= cost.oil * train
							take.iron -= cost.iron * train
							take.wood -= cost.wood * train
							take.food -= cost.food * train
							take.save()
						elif form.cleaned_data.get('t1') > 0:
							nex = army.t1.troop.training_time
							maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
							train = min(int(form.cleaned_data.get('t1')), maximum)
							new = Queue(troop = army.t1, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
							take = player.last_village.resources
							cost = army.t1.troop.training_cost
							take.oil -= cost.oil * train
							take.iron -= cost.iron * train
							take.wood -= cost.wood * train
							take.food -= cost.food * train
							take.save()
						new.save()
						bar = Barracks()
						bar.save()
						bar.queue.add(new)
						bar.save()
						tq = TrainingQueue(barracks = bar, next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )))		
					return redirect ('/center/')
			else:
				form = CampForm(player_id = player.id, lvl = buildinga.lvl)
			return render(request, 'game/camp.html', {'player': player, 'village_name' : village_name, 'resources': resources, 'warehouse': warehouse, 'silo' : silo,'field':field, 'oil': oil, 'iron':iron, 'wood':wood, 'food':food, 'production':production, 'cost_oil':cost_oil, 'cost_iron':cost_iron, 'cost_wood': cost_wood, 'cost_food':cost_food, 'upgrade_time':upgrade_time, 'description':description, 'picture':picture, 'pos':pos, 'ok':ok, 'unread_messages':count_messages(request), 'multi': True, 'form':form})
		if buildinga.building.name == 'Hangar':
			form = HangarForm(request.POST, player_id = player.id, lvl = buildinga.lvl)
			if request.method == 'POST':
				if form.is_valid():
					if player.tribe.name == 'Partisans':
						army = Partisan_troops.objects.get(id = 1)
					elif player.tribe.name == 'Russians':
						army = Russian_troops.objects.get(id = 1)
					elif player.tribe.name == 'Americans':
						army = American_troops.objects.get(id = 1)
					elif player.tribe.name == 'Brittish':
						army = Brittish_troops.objects.get(id = 1)
					elif player.tribe.name == 'Germans':
						army = German_troops.objects.get(id = 1)
					elif player.tribe.name == 'Japanese':
						army = Japanese_troops.objects.get(id = 1)
					if player.last_village.training_queue is not None:
						queue = player.last_village.training_queue
						if queue.barracks is not None:
							barracks = queue.hangar__set.order_by('-end_time')
							if barracks.end_time < datetime.utcnow().replace(tzinfo=utc):
								if form.cleaned_data.get('t2') > 0:
									nex = army.t2.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t2')), maximum)
									new = Queue(troop = army.t2, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t2.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
								elif form.cleaned_data.get('t3') > 0:
									nex = army.t3.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t3')), maximum)
									new = Queue(troop = army.t3, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t3.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
								elif form.cleaned_data.get('t4') > 0:
									nex = army.t4.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t4')), maximum)
									new = Queue(troop = army.t4, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t4.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
							else:
								if form.cleaned_data.get('t2') > 0:
									nex = army.t2.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t2')), maximum)
									new = Queue(troop = army.t2, quantity = int(train), start_time = barracks.end_time, end_time = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = barracks.end_time + timedelta(int( seconds = (int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = barracks.end_time, building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t2.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
								elif form.cleaned_data.get('t3') > 0:
									nex = army.t3.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t3')), maximum)
									new = Queue(troop = army.t3, quantity = int(train), start_time = barracks.end_time, end_time = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = barracks.end_time, building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t3.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
								elif form.cleaned_data.get('t4') > 0:
									nex = army.t4.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t4')), maximum)
									new = Queue(troop = army.t4, quantity = int(train), start_time = barracks.end_time, end_time = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = barracks.end_time, building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t4.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
							new.save()
							queue.add(new)
							queue.save()
						else:
							if form.cleaned_data.get('t2') > 0:
								nex = army.t2.troop.training_time
								maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
								train = min(int(form.cleaned_data.get('t2')), maximum)
								new = Queue(troop = army.t2, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
								take = player.last_village.resources
								cost = army.t2.troop.training_cost
								take.oil -= cost.oil * train
								take.iron -= cost.iron * train
								take.wood -= cost.wood * train
								take.food -= cost.food * train
								take.save()
							elif form.cleaned_data.get('t3') > 0:
								nex = army.t3.troop.training_time
								maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
								train = min(int(form.cleaned_data.get('t3')), maximum)
								new = Queue(troop = army.t3, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
								take = player.last_village.resources
								cost = army.t3.troop.training_cost
								take.oil -= cost.oil * train
								take.iron -= cost.iron * train
								take.wood -= cost.wood * train
								take.food -= cost.food * train
								take.save()
							elif form.cleaned_data.get('t4') > 0:
								nex = army.t4.troop.training_time
								maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
								train = min(int(form.cleaned_data.get('t4')), maximum)
								new = Queue(troop = army.t4, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
								take = player.last_village.resources
								cost = army.t4.troop.training_cost
								take.oil -= cost.oil * train
								take.iron -= cost.iron * train
								take.wood -= cost.wood * train
								take.food -= cost.food * train
								take.save()
							new.save()
							bar = Hangar()
							bar.save()
							bar.queue.add(new)
							bar.save()
					else:
						if form.cleaned_data.get('t2') > 0:
							nex = army.t2.troop.training_time
							maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
							train = min(int(form.cleaned_data.get('t2')), maximum)
							new = Queue(troop = army.t2, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
							take = player.last_village.resources
							cost = army.t2.troop.training_cost
							take.oil -= cost.oil * train
							take.iron -= cost.iron * train
							take.wood -= cost.wood * train
							take.food -= cost.food * train
							take.save()
						elif form.cleaned_data.get('t3') > 0:
							nex = army.t3.troop.training_time
							maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
							train = min(int(form.cleaned_data.get('t3')), maximum)
							new = Queue(troop = army.t3, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
							take = player.last_village.resources
							cost = army.t3.troop.training_cost
							take.oil -= cost.oil * train
							take.iron -= cost.iron * train
							take.wood -= cost.wood * train
							take.food -= cost.food * train
							take.save()
						elif form.cleaned_data.get('t4') > 0:
							nex = army.t4.troop.training_time
							maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
							train = min(int(form.cleaned_data.get('t4')), maximum)
							new = Queue(troop = army.t4, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
							take = player.last_village.resources
							cost = army.t4.troop.training_cost
							take.oil -= cost.oil * train
							take.iron -= cost.iron * train
							take.wood -= cost.wood * train
							take.food -= cost.food * train
							take.save()
						new.save()
						bar = Hangar()
						bar.save()
						bar.queue.add(new)
						bar.save()
						tq = TrainingQueue(hangar = bar, next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )))		
					return redirect ('/center/')
			else:
				form = HangarForm(player_id = player.id, lvl = buildinga.lvl)
			return render(request, 'game/camp.html', {'player': player, 'village_name' : village_name, 'resources': resources, 'warehouse': warehouse, 'silo' : silo,'field':field, 'oil': oil, 'iron':iron, 'wood':wood, 'food':food, 'production':production, 'cost_oil':cost_oil, 'cost_iron':cost_iron, 'cost_wood': cost_wood, 'cost_food':cost_food, 'upgrade_time':upgrade_time, 'description':description, 'picture':picture, 'pos':pos, 'ok':ok, 'unread_messages':count_messages(request), 'multi': True, 'form':form})
		if buildinga.building.name == 'Large camp':
			form = CampForm(request.POST, player_id = player.id, lvl = buildinga.lvl)
			if request.method == 'POST':
				
				if form.is_valid():
					
					if player.tribe.name == 'Partisans':
						army = Partisan_troops.objects.get(id = 1)
					elif player.tribe.name == 'Russians':
						army = Russian_troops.objects.get(id = 1)
					elif player.tribe.name == 'Americans':
						army = American_troops.objects.get(id = 1)
					elif player.tribe.name == 'Brittish':
						army = Brittish_troops.objects.get(id = 1)
					elif player.tribe.name == 'Germans':
						army = German_troops.objects.get(id = 1)
					elif player.tribe.name == 'Japanese':
						army = Japanese_troops.objects.get(id = 1)
						
					if player.last_village.training_queue is not None:
						queue = player.last_village.training_queue
						if queue.barracks is not None:
							barracks = queue.barracks_large__set.order_by('-end_time')
							if barracks.end_time < datetime.utcnow().replace(tzinfo=utc):
								if form.cleaned_data.get('t0') > 0:
									nex = army.t0.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									maximum /= 3
									train = min(int(form.cleaned_data.get('t0')), maximum)
									new = Queue(troop = army.t0, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t0.troop.training_cost
									take.oil -= cost.oil * train * 3
									take.iron -= cost.iron * train * 3
									take.wood -= cost.wood * train * 3
									take.food -= cost.food * train * 3
									take.save()
								elif form.cleaned_data.get('t1') > 0:
									nex = army.t1.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									maximum /= 3
									train = min(int(form.cleaned_data.get('t1')), maximum)
									new = Queue(troop = army.t1, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t1.troop.training_cost
									take.oil -= cost.oil * train * 3
									take.iron -= cost.iron * train * 3
									take.wood -= cost.wood * train * 3
									take.food -= cost.food * train * 3
									take.save()
							else:
								if form.cleaned_data.get('t0') > 0:
									nex = army.t0.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									maximum /= 3
									train = min(int(form.cleaned_data.get('t0')), maximum)
									new = Queue(troop = army.t0, quantity = int(train), start_time = barracks.end_time, end_time = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = barracks.end_time + timedelta(int( seconds = (int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = barracks.end_time, building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t0.troop.training_cost
									take.oil -= cost.oil * train * 3
									take.iron -= cost.iron * train * 3
									take.wood -= cost.wood * train * 3
									take.food -= cost.food * train * 3
									take.save()
								elif form.cleaned_data.get('t1') > 0:
									nex = army.t1.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									maximum /= 3
									train = min(int(form.cleaned_data.get('t1')), maximum)
									new = Queue(troop = army.t1, quantity = int(train), start_time = barracks.end_time, end_time = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = barracks.end_time, building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t1.troop.training_cost
									take.oil -= cost.oil * train * 3
									take.iron -= cost.iron * train * 3
									take.wood -= cost.wood * train * 3
									take.food -= cost.food * train * 3
									take.save()
							new.save()
							queue.add(new)
							queue.save()
						else:
							if form.cleaned_data.get('t0') > 0:
								nex = army.t0.troop.training_time
								maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
								maximum /= 3
								train = min(int(form.cleaned_data.get('t0')), maximum)
								new = Queue(troop = army.t0, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
								take = player.last_village.resources
								cost = army.t0.troop.training_cost
								take.oil -= cost.oil * train * 3
								take.iron -= cost.iron * train * 3
								take.wood -= cost.wood * train * 3
								take.food -= cost.food * train * 3
								take.save()
							elif form.cleaned_data.get('t1') > 0:
								nex = army.t1.troop.training_time
								maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
								maximum /= 3
								train = min(int(form.cleaned_data.get('t1')), maximum)
								new = Queue(troop = army.t1, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
								take = player.last_village.resources
								cost = army.t1.troop.training_cost
								take.oil -= cost.oil * train * 3
								take.iron -= cost.iron * train * 3
								take.wood -= cost.wood * train * 3
								take.food -= cost.food * train * 3
								take.save()
							new.save()
							bar = Barracks()
							bar.save()
							bar.queue.add(new)
							bar.save()
					else:
						if form.cleaned_data.get('t0') > 0:
							nex = army.t0.troop.training_time
							maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
							maximum /= 3
							train = min(int(form.cleaned_data.get('t0')), maximum)
							new = Queue(troop = army.t0, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
							take = player.last_village.resources
							cost = army.t0.troop.training_cost
							take.oil -= cost.oil * train * 3
							take.iron -= cost.iron * train * 3
							take.wood -= cost.wood * train * 3
							take.food -= cost.food * train * 3
							take.save()
						elif form.cleaned_data.get('t1') > 0:
							nex = army.t1.troop.training_time
							maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
							maximum /= 3
							train = min(int(form.cleaned_data.get('t1')), maximum)
							new = Queue(troop = army.t1, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
							take = player.last_village.resources
							cost = army.t1.troop.training_cost
							take.oil -= cost.oil * train * 3
							take.iron -= cost.iron * train * 3
							take.wood -= cost.wood * train * 3
							take.food -= cost.food * train * 3
							take.save()
						new.save()
						bar = Barracks()
						bar.save()
						bar.queue.add(new)
						bar.save()
						tq = TrainingQueue(barracks = bar, next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )))		
					return redirect ('/center/')
			else:
				form = CampForm(player_id = player.id, lvl = buildinga.lvl)
			cost.oil *= 3
			cost.iron *= 3
			cost.wood *= 3
			cost.food *= 3
			return render(request, 'game/camp.html', {'player': player, 'village_name' : village_name, 'resources': resources, 'warehouse': warehouse, 'silo' : silo,'field':field, 'oil': oil, 'iron':iron, 'wood':wood, 'food':food, 'production':production, 'cost_oil':cost_oil, 'cost_iron':cost_iron, 'cost_wood': cost_wood, 'cost_food':cost_food, 'upgrade_time':upgrade_time, 'description':description, 'picture':picture, 'pos':pos, 'ok':ok, 'unread_messages':count_messages(request), 'multi': True, 'form':form})
		if buildinga.building.name == 'Large hangar':
			form = HangarForm(request.POST, player_id = player.id, lvl = buildinga.lvl)
			if request.method == 'POST':
				if form.is_valid():
					if player.tribe.name == 'Partisans':
						army = Partisan_troops.objects.get(id = 1)
					elif player.tribe.name == 'Russians':
						army = Russian_troops.objects.get(id = 1)
					elif player.tribe.name == 'Americans':
						army = American_troops.objects.get(id = 1)
					elif player.tribe.name == 'Brittish':
						army = Brittish_troops.objects.get(id = 1)
					elif player.tribe.name == 'Germans':
						army = German_troops.objects.get(id = 1)
					elif player.tribe.name == 'Japanese':
						army = Japanese_troops.objects.get(id = 1)
					if player.last_village.training_queue is not None:
						queue = player.last_village.training_queue
						if queue.barracks is not None:
							barracks = queue.hangar_large__set.order_by('-end_time')
							if barracks.end_time < datetime.utcnow().replace(tzinfo=utc):
								if form.cleaned_data.get('t2') > 0:
									nex = army.t2.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									maximum /= 3
									train = min(int(form.cleaned_data.get('t2')), maximum)
									new = Queue(troop = army.t2, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t2.troop.training_cost
									take.oil -= cost.oil * train * 3
									take.iron -= cost.iron * train * 3
									take.wood -= cost.wood * train * 3
									take.food -= cost.food * train * 3
									take.save()
								elif form.cleaned_data.get('t3') > 0:
									nex = army.t3.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									maximum /= 3
									train = min(int(form.cleaned_data.get('t3')), maximum)
									new = Queue(troop = army.t3, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t3.troop.training_cost
									take.oil -= cost.oil * train * 3
									take.iron -= cost.iron * train * 3
									take.wood -= cost.wood * train * 3
									take.food -= cost.food * train * 3
									take.save()
								elif form.cleaned_data.get('t4') > 0:
									nex = army.t4.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									maximum /= 3
									train = min(int(form.cleaned_data.get('t4')), maximum)
									new = Queue(troop = army.t4, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t4.troop.training_cost
									take.oil -= cost.oil * train * 3
									take.iron -= cost.iron * train * 3
									take.wood -= cost.wood * train * 3
									take.food -= cost.food * train * 3
									take.save()
							else:
								if form.cleaned_data.get('t2') > 0:
									nex = army.t2.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									maximum /= 3
									train = min(int(form.cleaned_data.get('t2')), maximum)
									new = Queue(troop = army.t2, quantity = int(train), start_time = barracks.end_time, end_time = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = barracks.end_time + timedelta(int( seconds = (int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = barracks.end_time, building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t2.troop.training_cost
									take.oil -= cost.oil * train * 3
									take.iron -= cost.iron * train * 3
									take.wood -= cost.wood * train * 3
									take.food -= cost.food * train * 3
									take.save()
								elif form.cleaned_data.get('t3') > 0:
									nex = army.t3.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									maximum /= 3
									train = min(int(form.cleaned_data.get('t3')), maximum)
									new = Queue(troop = army.t3, quantity = int(train), start_time = barracks.end_time, end_time = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = barracks.end_time, building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t3.troop.training_cost
									take.oil -= cost.oil * train * 3
									take.iron -= cost.iron * train * 3 
									take.wood -= cost.wood * train * 3 
									take.food -= cost.food * train * 3
									take.save()
								elif form.cleaned_data.get('t4') > 0:
									nex = army.t4.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									maximum /= 3
									train = min(int(form.cleaned_data.get('t4')), maximum)
									new = Queue(troop = army.t4, quantity = int(train), start_time = barracks.end_time, end_time = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = barracks.end_time, building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t4.troop.training_cost
									take.oil -= cost.oil * train * 3
									take.iron -= cost.iron * train * 3
									take.wood -= cost.wood * train * 3
									take.food -= cost.food * train * 3
									take.save()
							new.save()
							queue.add(new)
							queue.save()
						else:
							if form.cleaned_data.get('t2') > 0:
								nex = army.t2.troop.training_time
								maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
								maximum /= 3
								train = min(int(form.cleaned_data.get('t2')), maximum)
								new = Queue(troop = army.t2, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
								take = player.last_village.resources
								cost = army.t2.troop.training_cost
								take.oil -= cost.oil * train * 3
								take.iron -= cost.iron * train * 3
								take.wood -= cost.wood * train * 3
								take.food -= cost.food * train * 3
								take.save()
							elif form.cleaned_data.get('t3') > 0:
								nex = army.t3.troop.training_time
								maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
								maximum /= 3
								train = min(int(form.cleaned_data.get('t3')), maximum)
								new = Queue(troop = army.t3, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
								take = player.last_village.resources
								cost = army.t3.troop.training_cost
								take.oil -= cost.oil * train * 3
								take.iron -= cost.iron * train * 3
								take.wood -= cost.wood * train * 3 
								take.food -= cost.food * train * 3
								take.save()
							elif form.cleaned_data.get('t4') > 0:
								nex = army.t4.troop.training_time
								maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
								maximum /= 3
								train = min(int(form.cleaned_data.get('t4')), maximum)
								new = Queue(troop = army.t4, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
								take = player.last_village.resources
								cost = army.t4.troop.training_cost
								take.oil -= cost.oil * train * 3
								take.iron -= cost.iron * train * 3
								take.wood -= cost.wood * train * 3
								take.food -= cost.food * train * 3
								take.save()
							new.save()
							bar = Hangar()
							bar.save()
							bar.queue.add(new)
							bar.save()
					else:
						if form.cleaned_data.get('t2') > 0:
							nex = army.t2.troop.training_time
							maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
							maximum /= 3
							train = min(int(form.cleaned_data.get('t2')), maximum)
							new = Queue(troop = army.t2, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
							take = player.last_village.resources
							cost = army.t2.troop.training_cost
							take.oil -= cost.oil * train * 3
							take.iron -= cost.iron * train * 3
							take.wood -= cost.wood * train * 3
							take.food -= cost.food * train * 3
							take.save()
						elif form.cleaned_data.get('t3') > 0:
							nex = army.t3.troop.training_time
							maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
							maximum /= 3
							train = min(int(form.cleaned_data.get('t3')), maximum)
							new = Queue(troop = army.t3, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
							take = player.last_village.resources
							cost = army.t3.troop.training_cost
							take.oil -= cost.oil * train * 3
							take.iron -= cost.iron * train * 3 
							take.wood -= cost.wood * train * 3
							take.food -= cost.food * train * 3
							take.save()
						elif form.cleaned_data.get('t4') > 0:
							nex = army.t4.troop.training_time
							maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
							maximum /= 3
							train = min(int(form.cleaned_data.get('t4')), maximum)
							new = Queue(troop = army.t4, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
							take = player.last_village.resources
							cost = army.t4.troop.training_cost 
							take.oil -= cost.oil * train * 3
							take.iron -= cost.iron * train * 3
							take.wood -= cost.wood * train * 3
							take.food -= cost.food * train * 3
							take.save()
						new.save()
						bar = Hangar()
						bar.save()
						bar.queue.add(new)
						bar.save()
						tq = TrainingQueue(hangar = bar, next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )))		
					return redirect ('/center/')
			else:
				form = HangarForm(player_id = player.id, lvl = buildinga.lvl)
			cost.oil *= 3
			cost.iron *= 3
			cost.wood *= 3
			cost.food *= 3
			return render(request, 'game/camp.html', {'player': player, 'village_name' : village_name, 'resources': resources, 'warehouse': warehouse, 'silo' : silo,'field':field, 'oil': oil, 'iron':iron, 'wood':wood, 'food':food, 'production':production, 'cost_oil':cost_oil, 'cost_iron':cost_iron, 'cost_wood': cost_wood, 'cost_food':cost_food, 'upgrade_time':upgrade_time, 'description':description, 'picture':picture, 'pos':pos, 'ok':ok, 'unread_messages':count_messages(request), 'multi': True, 'form':form})
		if buildinga.building.name == 'Port':
			form = PortForm(request.POST, player_id = player.id, lvl = buildinga.lvl)
			if request.method == 'POST':
				if form.is_valid():
					if player.tribe.name == 'Partisans':
						army = Partisan_troops.objects.get(id = 1)
					elif player.tribe.name == 'Russians':
						army = Russian_troops.objects.get(id = 1)
					elif player.tribe.name == 'Americans':
						army = American_troops.objects.get(id = 1)
					elif player.tribe.name == 'Brittish':
						army = Brittish_troops.objects.get(id = 1)
					elif player.tribe.name == 'Germans':
						army = German_troops.objects.get(id = 1)
					elif player.tribe.name == 'Japanese':
						army = Japanese_troops.objects.get(id = 1)
					if player.last_village.training_queue is not None:
						queue = player.last_village.training_queue
						if queue.barracks is not None:
							barracks = queue.port__set.order_by('-end_time')
							if barracks.end_time < datetime.utcnow().replace(tzinfo=utc):
								if form.cleaned_data.get('t5') > 0:
									nex = army.t5.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t5')), maximum)
									new = Queue(troop = army.t5, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t5.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
								elif form.cleaned_data.get('t6') > 0:
									nex = army.t6.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t6')), maximum)
									new = Queue(troop = army.t6, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t6.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
								elif form.cleaned_data.get('t7') > 0:
									nex = army.t7.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t7')), maximum)
									new = Queue(troop = army.t7, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t7.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
							else:
								if form.cleaned_data.get('t5') > 0:
									nex = army.t5.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t5')), maximum)
									new = Queue(troop = army.t5, quantity = int(train), start_time = barracks.end_time, end_time = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = barracks.end_time + timedelta(int( seconds = (int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = barracks.end_time, building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t5.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
								elif form.cleaned_data.get('t6') > 0:
									nex = army.t6.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t6')), maximum)
									new = Queue(troop = army.t6, quantity = int(train), start_time = barracks.end_time, end_time = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = barracks.end_time, building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t6.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
								elif form.cleaned_data.get('t7') > 0:
									nex = army.t7.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t7')), maximum)
									new = Queue(troop = army.t7, quantity = int(train), start_time = barracks.end_time, end_time = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = barracks.end_time, building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t7.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
							new.save()
							queue.add(new)
							queue.save()
						else:
							if form.cleaned_data.get('t5') > 0:
								nex = army.t5.troop.training_time
								maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
								train = min(int(form.cleaned_data.get('t5')), maximum)
								new = Queue(troop = army.t5, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
								take = player.last_village.resources
								cost = army.t5.troop.training_cost
								take.oil -= cost.oil * train
								take.iron -= cost.iron * train
								take.wood -= cost.wood * train
								take.food -= cost.food * train
								take.save()
							elif form.cleaned_data.get('t6') > 0:
								nex = army.t6.troop.training_time
								maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
								train = min(int(form.cleaned_data.get('t6')), maximum)
								new = Queue(troop = army.t6, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
								take = player.last_village.resources
								cost = army.t6.troop.training_cost
								take.oil -= cost.oil * train
								take.iron -= cost.iron * train
								take.wood -= cost.wood * train
								take.food -= cost.food * train
								take.save()
							elif form.cleaned_data.get('t7') > 0:
								nex = army.t7.troop.training_time
								maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
								train = min(int(form.cleaned_data.get('t7')), maximum)
								new = Queue(troop = army.t7, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
								take = player.last_village.resources
								cost = army.t7.troop.training_cost
								take.oil -= cost.oil * train
								take.iron -= cost.iron * train
								take.wood -= cost.wood * train
								take.food -= cost.food * train
								take.save()
							new.save()
							bar = Port()
							bar.save()
							bar.queue.add(new)
							bar.save()
					else:
						if form.cleaned_data.get('t5') > 0:
							nex = army.t5.troop.training_time
							maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
							train = min(int(form.cleaned_data.get('t5')), maximum)
							new = Queue(troop = army.t5, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
							take = player.last_village.resources
							cost = army.t5.troop.training_cost
							take.oil -= cost.oil * train
							take.iron -= cost.iron * train
							take.wood -= cost.wood * train
							take.food -= cost.food * train
							take.save()
						elif form.cleaned_data.get('t6') > 0:
							nex = army.t6.troop.training_time
							maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
							train = min(int(form.cleaned_data.get('t6')), maximum)
							new = Queue(troop = army.t6, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
							take = player.last_village.resources
							cost = army.t6.troop.training_cost
							take.oil -= cost.oil * train
							take.iron -= cost.iron * train
							take.wood -= cost.wood * train
							take.food -= cost.food * train
							take.save()
						elif form.cleaned_data.get('t7') > 0:
							nex = army.t7.troop.training_time
							maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
							train = min(int(form.cleaned_data.get('t7')), maximum)
							new = Queue(troop = army.t7, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
							take = player.last_village.resources
							cost = army.t7.troop.training_cost
							take.oil -= cost.oil * train
							take.iron -= cost.iron * train
							take.wood -= cost.wood * train
							take.food -= cost.food * train
							take.save()
						new.save()
						bar = Port()
						bar.save()
						bar.queue.add(new)
						bar.save()
						tq = TrainingQueue(port = bar, next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )))
					
					return redirect ('/center/')
			else:
				form = PortForm(player_id = player.id, lvl = buildinga.lvl)
			return render(request, 'game/camp.html', {'player': player, 'village_name' : village_name, 'resources': resources, 'warehouse': warehouse, 'silo' : silo,'field':field, 'oil': oil, 'iron':iron, 'wood':wood, 'food':food, 'production':production, 'cost_oil':cost_oil, 'cost_iron':cost_iron, 'cost_wood': cost_wood, 'cost_food':cost_food, 'upgrade_time':upgrade_time, 'description':description, 'picture':picture, 'pos':pos, 'ok':ok, 'unread_messages':count_messages(request), 'multi': True, 'form':form})
		if buildinga.building.name == 'Artilery mansion':
			form = ArtileryForm(request.POST, player_id = player.id, lvl = buildinga.lvl)
			if request.method == 'POST':
				if form.is_valid():
					if player.tribe.name == 'Partisans':
						army = Partisan_troops.objects.get(id = 1)
					elif player.tribe.name == 'Russians':
						army = Russian_troops.objects.get(id = 1)
					elif player.tribe.name == 'Americans':
						army = American_troops.objects.get(id = 1)
					elif player.tribe.name == 'Brittish':
						army = Brittish_troops.objects.get(id = 1)
					elif player.tribe.name == 'Germans':
						army = German_troops.objects.get(id = 1)
					elif player.tribe.name == 'Japanese':
						army = Japanese_troops.objects.get(id = 1)
					if player.last_village.training_queue is not None:
						queue = player.last_village.training_queue
						if queue.barracks is not None:
							barracks = queue.artilery__set.order_by('-end_time')
							if barracks.end_time < datetime.utcnow().replace(tzinfo=utc):
								if form.cleaned_data.get('t8') > 0:
									nex = army.t8.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t8')), maximum)
									new = Queue(troop = army.t8, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t8.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
								elif form.cleaned_data.get('t9') > 0:
									nex = army.t9.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t9')), maximum)
									new = Queue(troop = army.t9, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t9.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
								elif form.cleaned_data.get('t10') > 0:
									nex = army.t10.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t10')), maximum)
									new = Queue(troop = army.t10, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t10.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
								elif form.cleaned_data.get('t11') > 0:
									nex = army.t11.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t11')), maximum)
									new = Queue(troop = army.t11, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t11.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
							else:
								if form.cleaned_data.get('t8') > 0:
									nex = army.t8.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t8')), maximum)
									new = Queue(troop = army.t8, quantity = int(train), start_time = barracks.end_time, end_time = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = barracks.end_time + timedelta(int( seconds = (int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = barracks.end_time, building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t8.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
								elif form.cleaned_data.get('t9') > 0:
									nex = army.t9.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t9')), maximum)
									new = Queue(troop = army.t9, quantity = int(train), start_time = barracks.end_time, end_time = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = barracks.end_time, building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t9.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
								elif form.cleaned_data.get('t10') > 0:
									nex = army.t10.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t10')), maximum)
									new = Queue(troop = army.t10, quantity = int(train), start_time = barracks.end_time, end_time = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = barracks.end_time, building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t10.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
								elif form.cleaned_data.get('t11') > 0:
									nex = army.t11.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t11')), maximum)
									new = Queue(troop = army.t11, quantity = int(train), start_time = barracks.end_time, end_time = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = barracks.end_time, building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t11.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
							new.save()
							queue.add(new)
							queue.save()
						else:
							if form.cleaned_data.get('t8') > 0:
								nex = army.t8.troop.training_time
								maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
								train = min(int(form.cleaned_data.get('t8')), maximum)
								new = Queue(troop = army.t8, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
								take = player.last_village.resources
								cost = army.t8.troop.training_cost
								take.oil -= cost.oil * train
								take.iron -= cost.iron * train
								take.wood -= cost.wood * train
								take.food -= cost.food * train
								take.save()
							elif form.cleaned_data.get('t9') > 0:
								nex = army.t9.troop.training_time
								maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
								train = min(int(form.cleaned_data.get('t9')), maximum)
								new = Queue(troop = army.t9, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
								take = player.last_village.resources
								cost = army.t9.troop.training_cost
								take.oil -= cost.oil * train
								take.iron -= cost.iron * train
								take.wood -= cost.wood * train
								take.food -= cost.food * train
								take.save()
							elif form.cleaned_data.get('t10') > 0:
								nex = army.t10.troop.training_time
								maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
								train = min(int(form.cleaned_data.get('t10')), maximum)
								new = Queue(troop = army.t10, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
								take = player.last_village.resources
								cost = army.t10.troop.training_cost
								take.oil -= cost.oil * train
								take.iron -= cost.iron * train
								take.wood -= cost.wood * train
								take.food -= cost.food * train
								take.save()
							elif form.cleaned_data.get('t11') > 0:
								nex = army.t11.troop.training_time
								maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
								train = min(int(form.cleaned_data.get('t11')), maximum)
								new = Queue(troop = army.t11, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
								take = player.last_village.resources
								cost = army.t11.troop.training_cost
								take.oil -= cost.oil * train
								take.iron -= cost.iron * train
								take.wood -= cost.wood * train
								take.food -= cost.food * train
								take.save()
							new.save()
							bar = Artilery()
							bar.save()
							bar.queue.add(new)
							bar.save()
					else:
						if form.cleaned_data.get('t8') > 0:
							nex = army.t8.troop.training_time
							maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
							train = min(int(form.cleaned_data.get('t8')), maximum)
							new = Queue(troop = army.t8, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
							take = player.last_village.resources
							cost = army.t8.troop.training_cost
							take.oil -= cost.oil * train
							take.iron -= cost.iron * train
							take.wood -= cost.wood * train
							take.food -= cost.food * train
							take.save()
						elif form.cleaned_data.get('t9') > 0:
							nex = army.t9.troop.training_time
							maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
							train = min(int(form.cleaned_data.get('t9')), maximum)
							new = Queue(troop = army.t9, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
							take = player.last_village.resources
							cost = army.t9.troop.training_cost
							take.oil -= cost.oil * train
							take.iron -= cost.iron * train
							take.wood -= cost.wood * train
							take.food -= cost.food * train
							take.save()
						elif form.cleaned_data.get('t10') > 0:
							nex = army.t10.troop.training_time
							maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
							train = min(int(form.cleaned_data.get('t10')), maximum)
							new = Queue(troop = army.t10, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
							take = player.last_village.resources
							cost = army.t10.troop.training_cost
							take.oil -= cost.oil * train
							take.iron -= cost.iron * train
							take.wood -= cost.wood * train
							take.food -= cost.food * train
							take.save()
						elif form.cleaned_data.get('t11') > 0:
							nex = army.t11.troop.training_time
							maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
							train = min(int(form.cleaned_data.get('t11')), maximum)
							new = Queue(troop = army.t11, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
							take = player.last_village.resources
							cost = army.t11.troop.training_cost
							take.oil -= cost.oil * train
							take.iron -= cost.iron * train
							take.wood -= cost.wood * train
							take.food -= cost.food * train
							take.save()
						new.save()
						bar = Artilery()
						bar.save()
						bar.queue.add(new)
						bar.save()
						tq = TrainingQueue(port = bar, next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )))
					
					return redirect ('/center/')
			else:
				form = AmmunitionForm(player_id = player.id, lvl = buildinga.lvl)
			return render(request, 'game/camp.html', {'player': player, 'village_name' : village_name, 'resources': resources, 'warehouse': warehouse, 'silo' : silo,'field':field, 'oil': oil, 'iron':iron, 'wood':wood, 'food':food, 'production':production, 'cost_oil':cost_oil, 'cost_iron':cost_iron, 'cost_wood': cost_wood, 'cost_food':cost_food, 'upgrade_time':upgrade_time, 'description':description, 'picture':picture, 'pos':pos, 'ok':ok, 'unread_messages':count_messages(request), 'multi': True, 'form':form})
		if (buildinga.building.name == 'Parliament' or buildinga.building.name == 'Summer residence') and buildinga.buinding.lvl > 10:
			form = ParliForm(request.POST, player_id = player.id, lvl = buildinga.lvl)
			if request.method == 'POST':
				
				if form.is_valid():
					
					if player.tribe.name == 'Partisans':
						army = Partisan_troops.objects.get(id = 1)
					elif player.tribe.name == 'Russians':
						army = Russian_troops.objects.get(id = 1)
					elif player.tribe.name == 'Americans':
						army = American_troops.objects.get(id = 1)
					elif player.tribe.name == 'Brittish':
						army = Brittish_troops.objects.get(id = 1)
					elif player.tribe.name == 'Germans':
						army = German_troops.objects.get(id = 1)
					elif player.tribe.name == 'Japanese':
						army = Japanese_troops.objects.get(id = 1)
						
					if player.last_village.training_queue is not None:
						queue = player.last_village.training_queue
						if queue.barracks is not None:
							barracks = queue.parli__set.order_by('-end_time')
							if barracks.end_time < datetime.utcnow().replace(tzinfo=utc):
								if form.cleaned_data.get('t0') > 0:
									nex = army.t0.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t0')), maximum)
									new = Queue(troop = army.t0, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t0.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
								elif form.cleaned_data.get('t1') > 0:
									nex = army.t1.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t1')), maximum)
									new = Queue(troop = army.t1, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t1.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
							else:
								if form.cleaned_data.get('t0') > 0:
									nex = army.t0.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t0')), maximum)
									new = Queue(troop = army.t0, quantity = int(train), start_time = barracks.end_time, end_time = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = barracks.end_time + timedelta(int( seconds = (int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = barracks.end_time, building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t0.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
								elif form.cleaned_data.get('t1') > 0:
									nex = army.t1.troop.training_time
									maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
									train = min(int(form.cleaned_data.get('t1')), maximum)
									new = Queue(troop = army.t1, quantity = int(train), start_time = barracks.end_time, end_time = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = barracks.end_time + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = barracks.end_time, building_lvl = buildinga.lvl)
									take = player.last_village.resources
									cost = army.t1.troop.training_cost
									take.oil -= cost.oil * train
									take.iron -= cost.iron * train
									take.wood -= cost.wood * train
									take.food -= cost.food * train
									take.save()
							new.save()
							queue.add(new)
							queue.save()
						else:
							if form.cleaned_data.get('t0') > 0:
								nex = army.t0.troop.training_time
								maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
								train = min(int(form.cleaned_data.get('t0')), maximum)
								new = Queue(troop = army.t0, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
								take = player.last_village.resources
								cost = army.t0.troop.training_cost
								take.oil -= cost.oil * train
								take.iron -= cost.iron * train
								take.wood -= cost.wood * train
								take.food -= cost.food * train
								take.save()
							elif form.cleaned_data.get('t1') > 0:
								nex = army.t1.troop.training_time
								maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
								train = min(int(form.cleaned_data.get('t1')), maximum)
								new = Queue(troop = army.t1, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
								take = player.last_village.resources
								cost = army.t1.troop.training_cost
								take.oil -= cost.oil * train
								take.iron -= cost.iron * train
								take.wood -= cost.wood * train
								take.food -= cost.food * train
								take.save()
							new.save()
							bar = Parli()
							bar.save()
							bar.queue.add(new)
							bar.save()
					else:
						if form.cleaned_data.get('t0') > 0:
							nex = army.t0.troop.training_time
							maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
							train = min(int(form.cleaned_data.get('t0')), maximum)
							new = Queue(troop = army.t0, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
							take = player.last_village.resources
							cost = army.t0.troop.training_cost
							take.oil -= cost.oil * train
							take.iron -= cost.iron * train
							take.wood -= cost.wood * train
							take.food -= cost.food * train
							take.save()
						elif form.cleaned_data.get('t1') > 0:
							nex = army.t1.troop.training_time
							maximum = min(min(player.last_village.resources.oil // army.t0.troop.training_cost.oil, player.last_village.resources.iron // army.t0.troop.training_cost.iron), min(player.last_village.resources.wood // army.t0.troop.training_cost.wood, player.last_village.resources.food // army.t0.troop.training_cost.food))
							train = min(int(form.cleaned_data.get('t1')), maximum)
							new = Queue(troop = army.t1, quantity = int(train), start_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), end_time = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl)  * int(train))), next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )), last_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0), building_lvl = buildinga.lvl)
							take = player.last_village.resources
							cost = army.t1.troop.training_cost
							take.oil -= cost.oil * train
							take.iron -= cost.iron * train
							take.wood -= cost.wood * train
							take.food -= cost.food * train
							take.save()
						new.save()
						bar = Parli()
						bar.save()
						bar.queue.add(new)
						bar.save()
						tq = TrainingQueue(parli = bar, next_update = datetime.utcnow().replace(tzinfo=utc).replace(microsecond=0) + timedelta(seconds = int((int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600) * (0.9**buildinga.lvl) )))		
					return redirect ('/center/')
			else:
				form = ParliForm(player_id = player.id, lvl = buildinga.lvl)
			return render(request, 'game/camp.html', {'player': player, 'village_name' : village_name, 'resources': resources, 'warehouse': warehouse, 'silo' : silo,'field':field, 'oil': oil, 'iron':iron, 'wood':wood, 'food':food, 'production':production, 'cost_oil':cost_oil, 'cost_iron':cost_iron, 'cost_wood': cost_wood, 'cost_food':cost_food, 'upgrade_time':upgrade_time, 'description':description, 'picture':picture, 'pos':pos, 'ok':ok, 'unread_messages':count_messages(request), 'multi': True, 'form':form})
		return render(request, 'game/building.html', {'player': player, 'village_name' : village_name, 'resources': resources, 'warehouse': warehouse, 'silo' : silo,'field':field, 'oil': oil, 'iron':iron, 'wood':wood, 'food':food, 'production':production, 'cost_oil':cost_oil, 'cost_iron':cost_iron, 'cost_wood': cost_wood, 'cost_food':cost_food, 'upgrade_time':upgrade_time, 'description':description, 'picture':picture, 'pos':pos, 'ok':ok, 'unread_messages':count_messages(request)})
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
		return render(request, 'game/new-building.html', {'player': player, 'village_name' : village_name, 'resources': resources, 'warehouse': warehouse, 'silo' : silo, 'mozne':mozne, 'pos':pos, 'oil': oil, 'iron':iron, 'wood':wood, 'food':food, 'production':production, 'unread_messages':count_messages(request)})

@login_required			
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

@login_required	
def build(request,pos,bui):
	if bui == 'heros-birth-house':
		bui = 'hero-s-birth-house'
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
	print(buildinga.building)
	cena = building.models.Building.objects.filter(name = buildinga.building)
	cena = cena[0].cost.filter(level = 1)
	cena = cena[0]
	if resources.oil >= cena.oil and resources.iron >= cena.iron and resources.wood >= cena.wood and resources.food >= cena.food and player.last_village.free_crop >= cena.cost + 1:
		setattr(player.last_village.center, pos, buildinga)
		if buildinga.building.name == 'Parliament':
			player.parliament = True
			player.save()
		player.last_village.center.save()
		upgrade_building(request, pos)
		return redirect('/center')
	else:
		# TODO Remove building
		return redirect('/center')
		
@login_required		
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
	ycoords = ycoords[::-1]
	village = []
	image = []
	ok = []
	player = Player.objects.get(user = request.user)
	for i in range(7):
		for j in range (7):
			try:
				selo = Village.objects.filter(location_latitude = xcoords[j], location_longitude = ycoords[i])[0]
				village.append(selo)
				if selo.population > 0:
					image.append('/media/villages/village.png')
				else:
					image.append('/media/villages/empty-village.png')
				ok.append("1")
			except Exception:
				try:
					selo = Oasis.objects.filter(location_latitude = xcoords[j], location_longitude = ycoords[i])[0]
					village.append(selo)
					image.append('/media/villages/oasis.png')
					ok.append("1")
				except:
					ok.append("0")
					village.append(0)
					image.append('/media/villages/empty.png')
	villages = zip(village,image,ok)
	return render(request, 'game/map.html', {'villages':villages, 'player':player, 'unread_messages':count_messages(request), 'x':x, 'y':y})
	
@login_required			
def map_zero(request):
	user = request.user
	player = Player.objects.get(user = user)
	last = player.last_village
	return redirect('/map/x='+str(last.location_latitude)+'y='+str(last.location_longitude)+'/')
	
@login_required	
def gold(request):
	if Player.objects.get(user = request.user).gold < 0:
		ok = False
	else:
		ok = True
	return render(request,'game/gold.html', {'player':Player.objects.get(user = request.user), 'unread_messages':count_messages(request), 'ok':ok}) # TODO expires in template
	
@login_required		
def buy(request,arg):
	if arg == 'club':
		player = Player.objects.get(user = request.user)
		if player.gold >= 100 or player.gold < 0:
			player.gold -= 100
			player.bonuses.gold_club = True
			player.bonuses.save()
			player.save()
	if arg == 'plus':
		player = Player.objects.get(user = request.user)
		if player.gold >= 10 or player.gold < 0:
			player.gold -= 10
			if player.bonuses.plus_account < datetime.utcnow().replace(tzinfo=utc):
				player.bonuses.plus_account = datetime.utcnow().replace(tzinfo=utc) + timedelta(days = 7)
			else:
				player.bonuses.plus_account += timedelta(days = 7)
			player.bonuses.save()
			player.save()
	if arg  == 'oil':
		player = Player.objects.get(user = request.user)
		if player.gold >= 5 or player.gold < 0:
			player.gold -= 5
			if player.bonuses.oil_bonus_production < datetime.utcnow().replace(tzinfo=utc):
				player.bonuses.oil_bonus_production = datetime.utcnow().replace(tzinfo=utc) + timedelta(days = 7)
			else:
				player.bonuses.oil_bonus_production += timedelta(days = 7)
			player.bonuses.save()
			player.save()
	if arg == 'iron':
		player = Player.objects.get(user = request.user)
		if player.gold >= 5 or player.gold < 0:
			player.gold -= 5
			if player.bonuses.iron_bonus_production < datetime.utcnow().replace(tzinfo=utc):
				player.bonuses.iron_bonus_production = datetime.utcnow().replace(tzinfo=utc) + timedelta(days = 7)
			else:
				player.bonuses.iron_bonus_production += timedelta(days = 7)
			player.bonuses.save()
			player.save()
	if arg == 'wood':
		player = Player.objects.get(user = request.user)
		if player.gold >= 5 or player.gold < 0:
			player.gold -= 5
			if player.bonuses.wood_bonus_production < datetime.utcnow().replace(tzinfo=utc):
				player.bonuses.wood_bonus_production = datetime.utcnow().replace(tzinfo=utc) + timedelta(days = 7)
			else:
				player.bonuses.wood_bonus_production += timedelta(days = 7)
			player.bonuses.save()
			player.save()
	if arg == 'food':
		player = Player.objects.get(user = request.user)
		if player.gold >= 5 or player.gold < 0:
			player.gold -= 5
			if player.bonuses.food_bonus_production < datetime.utcnow().replace(tzinfo=utc):
				player.bonuses.food_bonus_production = datetime.utcnow().replace(tzinfo=utc) + timedelta(days = 7)
			else:
				player.bonuses.food_bonus_production += timedelta(days = 7)
			player.bonuses.save()
			player.save()
	if arg == 'food2':
		pass
	if arg == 'build':
		player = Player.objects.get(user = request.user)
		if player.last_village.field_1 is not None or player.last_village.building_1 is not None and player.gold >= 2 or player.gold < 0:
			counter = 0
			try:
				player.last_village.field_1.end = datetime.utcnow().replace(tzinfo=utc)
				player.last_village.field_1.save()
			except Exception:
				counter +=1
			try:
				player.last_village.field_2.end = datetime.utcnow().replace(tzinfo=utc)
				player.last_village.field_2.save()
			except Exception:
				counter +=1
			try:
				player.last_village.building_1.end = datetime.utcnow().replace(tzinfo=utc)
				player.last_village.building_1.save()
			except Exception:
				counter +=1
			try:
				player.last_village.building_2.end = datetime.utcnow().replace(tzinfo=utc)
				player.last_village.building_2.save()
			except Exception:
				counter +=1
			player.last_village.save()
			if counter < 4:
				player.gold -= 2
			player.save()
	if arg == 'upgrade':
		pass
	if arg == 'revive':
		pass
	if arg == 'heal':
		pass
	if arg == 'trade':
		pass
	if arg == '30':
		player = Player.objects.get(user = request.user)
		player.gold += 30
		player.save()
	if arg == '60':
		player = Player.objects.get(user = request.user)
		player.gold += 60
		player.save()
	if arg == '120':
		player = Player.objects.get(user = request.user)
		player.gold += 120
		player.save()
	if arg == '300':
		player = Player.objects.get(user = request.user)
		player.gold += 300
		player.save()
	if arg == '750':
		player = Player.objects.get(user = request.user)
		player.gold += 750
		player.save()
	if arg == '2500':
		player = Player.objects.get(user = request.user)
		player.gold += 2500
		player.save()
	if arg == '7000':
		player = Player.objects.get(user = request.user)
		player.gold += 7000
		player.save()
	if arg == 'unlimited':
		player = Player.objects.get(user = request.user)
		player.gold = -1
		player.save()
	sleep(1)
	return redirect('/fields/')

def get_bonus(i):
	if i== 1:
		return 'oil'
	elif i == 2:
		return 'iron'
	elif i == 3:
		return 'wood'
	else:
		return 'food'

@login_required		
def village_view(request,x,y):
	player = Player.objects.get(user = request.user)
	x = int(x)
	y = int(y)
	try:
		selo = Village.objects.filter(location_latitude = x, location_longitude = y)[0]
		return render(request, 'game/village.html', {'village':selo, 'player':player, 'unread_messages':count_messages(request), 'x':x, 'y':y})
	except Exception:
		try:
			selo = Oasis.objects.filter(location_latitude = x, location_longitude = y)[0]
			
			army = selo.army.all()[0]
			l = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13']
			names = ['Mosquito', 'Ant', 'Fly', 'Beatle', 'Spider', 'Rat', 'Snake', 'Eagle', 'Wolf', 'Cougar', 'Brown bear', 'Tiger', 'Shark', 'Cow']
			ll = []
			namess = []
			for i in range (14):
				if getattr(army,l[i]).count > 0:
					ll.append(getattr(army,l[i]).count)
					namess.append(names[i])
			troops = zip(ll,namess)
			bonuses = []
			bonuses.append(get_bonus(selo.bonus_1))
			if selo.bonus_2 is not None:
				bonuses.append(get_bonus(selo.bonus_2))
			return render(request, 'game/oasis.html', {'village':selo, 'player':player, 'unread_messages':count_messages(request), 'troops':troops, 'bonuses':bonuses, 'x':x, 'y':y})
		except:
			return redirect('/map/x='+str(x)+'y='+str(y)+'/')
			
