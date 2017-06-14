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
from world.init_troops import initialize as initialize_troops
from world.functions import *
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime
import operator
from django.contrib.auth.decorators import login_required
import building.models 
import time
from django.utils.timezone import utc

def register(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save(commit = False)
			user.is_active = True
			user.save()
			u_id = user.id
			hero = Hero()
			hero.name = form.cleaned_data.get('username')
			hero.save()
			hero_id = hero.id
			player = Player()
			player.user = User.objects.get(id = u_id)
			player.name = form.cleaned_data.get('username')
			player.hero = Hero.objects.get(id = hero_id)
			player.tribe = Tribe.objects.get(name = form.cleaned_data.get('select_tribe'))
			bonus = Bonus()
			bonus.gold_club = False
			bonus.save()
			bon_id = bonus.pk
			player.bonuses=Bonus.objects.get(id = bon_id)
			player.old_rank = 2
			player.location = form.cleaned_data.get('start_location')
			player.activation_key = account_activation_token.make_token(user)
			print(urlsafe_base64_encode(force_bytes(user.pk)))
			player.save()
			current_site = get_current_site(request)
			subject = 'Activate Your MySite Account'
			message = render_to_string('game/activation_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
			})
			user.email_user(subject, message)
				
			return redirect('/login/')
			
	else:
		form = SignUpForm()
	return render(request, 'game/register.html', {'form': form})
	
def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		player = Player.objects.get(user = user)
		player.is_active = True
		user.save()
		if player.location == 'nw':
			village = Village.objects.filter(typ = VillageType.objects.get(id = 1),  population = 0, location_latitude__lte = -1, location_longitude__gte = 1)
		elif player.location == 'ne':
			village = Village.objects.filter(location_latitude__gte = 1, location_longitude__gte = 1, typ = VillageType.objects.get(id = 1),  population = 0)
		elif player.location == 'se':
			village = Village.objects.filter(location_latitude__gte = 1, location_longitude__lte = -1, typ = VillageType.objects.get(id = 1),  population = 0)
		elif player.location == 'sw':
			village = Village.objects.filter(location_latitude__lte = -1, location_longitude__lte = -1, typ = VillageType.objects.get(id = 1),  population = 0)
		best = village[0]
		for selo in village:
			if best.location_latitude**2 + best.location_longitude**2 > selo.location_latitude**2 + selo.location_longitude**2:
				best = selo
		player.villages.add(best)
		player.last_village = best
		player.last_update = datetime.utcnow().replace(tzinfo=utc)
		best.name = player.user.username+"'s village"
		best.population = 2
		village_start(player, best)
		player.save()
		return redirect('/login/')
	else:
		return render(request, 'game/activation_invalid.html')
		
def login(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		return redirect('/fields/')
	else:
		return render(request, 'game/login.html')

def init_map():
	start = time.time()
	from django.contrib.sites.models import Site
	if Site.objects.count() < 2:	
		
		new_site = Site.objects.create(domain=settings.URL, name=settings.URL)
		print new_site.id
	if Village.objects.count() == 0:
		print(Village.objects.count())
		map_init()
	if building.models.Building.objects.count() == 0:
		buildings_init()
	if Tribe.objects.count() == 0:
		tribe_init()
	if building.models.Field.objects.count() == 0:
		fields_init()
	if Troop.objects.count() == 0:
		initialize_troops()
	end = time.time()
	print(end-start)
	return redirect('/')
