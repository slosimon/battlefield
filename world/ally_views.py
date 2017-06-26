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
from django.http import Http404 

def count_messages(request):
	player = Player.objects.get(user = request.user)
	return len(Message.objects.filter(read = False, recipent = player))

@login_required	
def create(request):
	player = Player.objects.get(user = request.user)
	if request.method == 'POST':
		form = AllyForm(request.POST)
		if form.is_valid():
			leader = Ally_leadership.objects.create(leader = player, position = 'Founder', mm_rights = True, diplomacy = True)
			ally = Alliance.objects.create(name = form.cleaned_data.get('name'), short_name = form.cleaned_data.get('short_name'), old_population = player.population)
			ally.leadership.add(leader)
			ally.member.add(player)
			ally.save()
			player.in_ally = True
			player.save()
			return redirect ('/ally/')
	else:
		form = AllyForm()
	return render(request, 'game/new_ally.html', {'player':player, 'unread_messages':count_messages(request), 'form':form})

@login_required
def ally(request):
	player = Player.objects.get(user = request.user)
	if player.in_ally:
		ally = player.alliance_set.all()
		ally = ally[0]
		members = ally.member.order_by('-population')
		count = len(members)
		leaders = ally.leadership.all()
		return render(request, 'game/ally.html', {'player':player, 'ally':ally, 'members':members, 'count':count, 'leadership':leaders})
	else:
		return redirect('/fields/')

@login_required		
def invitations(request):
	player = Player.objects.get(user = request.user)
	invitations = Invitation.objects.filter(invited = player)
	return render(request, 'game/invitations.html', {'invitationset':invitations, 'player':player})

@login_required	
def invitation_action(request, inv, action):
	player = Player.objects.get(user = request.user)
	invitations = Invitation.objects.get(id = inv)
	if invitations.invited == player:
		if action == "accept":
			player.in_ally = True
			invitations.ally.member.add(player)
			invitations.ally.save()
			player.save()
			invitations.delete()
		elif action== "reject":
			invitations.delete()
		else:
			return redirect('/fields/')
	return redirect('/ally/')

@login_required	
def invite(request):
	player = Player.objects.get(user = request.user)
	form = InviteForm(request.POST)
	ally = player.alliance_set.all()
	ally = ally[0]
	validator = False
	leaders = ally.leadership.all()
	for leader in leaders:
		print(leader.leader.id, player.id)
		if leader.leader == player and leader.invite:
			validator = True
	print(validator)
	if validator:
		if request.method == 'POST':
			if form.is_valid():
				username = form.cleaned_data.get('player')
				user = User.objects.get(username = username)
				invited = Player.objects.get(user= user)
				bar = Invitation.objects.create(ally = ally, invited = invited)
				return redirect ('/ally/')
		else:
			form = InviteForm()
		return render(request, 'game/invite.html', {'player':player, 'form':form})
	raise Http404

@login_required	
def profile(request):
	player = Player.objects.get(user = request.user)
	form = ProfileForm(request.POST)
	ally = player.alliance_set.all()
	ally = ally[0]
	validator = False
	leaders = ally.leadership.all()
	for leader in leaders:
		print(leader.leader.id, player.id)
		if leader.leader == player and leader.profile:
			validator = True
	print(validator)
	if validator:
		if request.method == 'POST':
			if form.is_valid():
				profile = form.cleaned_data.get('profile')
				ally.profile = profile
				ally.save()
				return redirect ('/ally/')
		else:
			form = ProfileForm()
		return render(request, 'game/profile.html', {'player':player, 'form':form})
	raise Http404

@login_required	
def new_leader(request):
	player = Player.objects.get(user = request.user)
	form = LeaderForm(request.POST)
	ally = player.alliance_set.all()
	ally = ally[0]
	validator = False
	leaders = ally.leadership.all()
	for leader in leaders:
		print(leader.leader.id, player.id)
		if leader.leader == player and leader.set_leader:
			validator = True
	print(validator)
	if validator:
		if request.method == 'POST':
			if form.is_valid():
				leader = form.cleaned_data.get('leader')
				position = form.cleaned_data.get('position')
				diplomacy = form.cleaned_data.get('diplomacy_rights')
				invite = form.cleaned_data.get('invite')
				set_leader = form.cleaned_data.get('set_leader')
				mm_rights = form.cleaned_data.get('mm_rights')
				profile = form.cleaned_data.get('profile')
				kick = form.cleaned_data.get('kick')
				user = User.objects.get(username = leader)
				leader = Player.objects.get(user= user)
				new = Ally_leadership.objects.create(leader = leader, position = position, diplomacy = diplomacy, invite = invite, set_leader = set_leader, profile = profile, kick = kick, mm_rights = mm_rights)
				ally.leadership.add(new)
				ally.save()
				return redirect ('/ally/')
		else:
			form = LeaderForm()
		return render(request, 'game/new_leader.html', {'player':player, 'form':form})
	raise Http404

@login_required	
def edit_leader(request, lea):
	player = Player.objects.get(user = request.user)
	form = LeaderEditForm(request.POST)
	ally = player.alliance_set.all()
	ally = ally[0]
	validator = False
	leaders = ally.leadership.all()
	for leader in leaders:
		print(leader.leader.id, player.id)
		if leader.leader == player and leader.set_leader:
			validator = True
	print(validator)
	if validator:
		new = Ally_leadership.objects.get(id = lea)
		if request.method == 'POST':
			if form.is_valid():
				position = form.cleaned_data.get('position')
				diplomacy = form.cleaned_data.get('diplomacy_rights')
				invite = form.cleaned_data.get('invite')
				set_leader = form.cleaned_data.get('set_leader')
				mm_rights = form.cleaned_data.get('mm_rights')
				profile = form.cleaned_data.get('profile')
				kick = form.cleaned_data.get('kick')
				user = User.objects.get(username = new.leader.user.username)
				leader = Player.objects.get(user= user)
				
				new.position = position
				new.diplomacy = diplomacy
				new.invite = invite
				new.set_leader = set_leader
				new.profile = profile
				new.kick = kick
				new.mm_rights = mm_rights
				new.save()
				ally.save()
				return redirect ('/ally/')
		else:
			from django.forms import widgets
			form = LeaderEditForm(initial={'leader': new.leader, 'position':new.position, 'diplomacy_rights':new.diplomacy, 'invite':new.invite, 'set_leader': new.set_leader, 'profile':new.profile, 'kick':new.kick, 'mm_rights':new.mm_rights})
		return render(request, 'game/edit_leader.html', {'player':player, 'form':form})
	raise Http404	

@login_required	
def edit_leaders(request):
	player = Player.objects.get(user = request.user)
	ally = player.alliance_set.all()
	ally = ally[0]
	validator = False
	leaders = ally.leadership.all()
	for leader in leaders:
		print(leader.leader.id, player.id)
		if leader.leader == player and leader.set_leader:
			validator = True
	print(validator)
	if validator:
		return render(request, 'game/edit_leaders.html', {'leaders':leaders})
	raise Http404

@login_required	
def leave(request):
	player = Player.objects.get(user = request.user)
	ally = player.alliance_set.all()
	ally = ally[0]
	form = ConfirmationForm(request.POST)
	if request.method == 'POST':
		if form.is_valid():
			print(form.cleaned_data.get('password'))
			if player.user.check_password(form.cleaned_data.get('password')):
				ally.member.remove(player)
				ally.save()
				player.in_ally = False
				player.save()
				return redirect ('/fields/')
			else:
				form = ConfirmationForm()
				return render(request, 'game/leave_ally.html', {'ally':ally, 'form':form})
	else:
		form = ConfirmationForm()
		return render(request, 'game/leave_ally.html', {'ally':ally, 'form':form})
		
# TODO kick, stats!
