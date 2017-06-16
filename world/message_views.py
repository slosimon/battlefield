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
from precise_bbcode.bbcode import get_parser

from slugify import slugify

def count_messages(request):
	player = Player.objects.get(user = request.user)
	return len(Message.objects.filter(read = False, recipent = player))

@login_required
def send(request):
	player = Player.objects.get(user = request.user)
	if request.method == 'POST':
		form = MessageForm(request.POST)
		if form.is_valid():
			parser = get_parser()
			print(form.cleaned_data.get('recipent'))
			string = form.cleaned_data.get('recipent')
			user = User.objects.filter(username = string)
			if len(user) > 0:
				Message.objects.create(sender = player, recipent = Player.objects.filter(user=user)[0], subject = form.cleaned_data.get('subject'), content = (form.cleaned_data.get('message')), timestamp = datetime.utcnow().replace(tzinfo=utc))
			elif form.cleaned_data.get('recipent') == '[MM]':
				pass # TODO MM
			return redirect ('/messages/inbox/')
	else:
		form = MessageForm()
	return render(request, 'game/new_message.html', {'player':player, 'unread_messages':count_messages(request), 'form':form})
	
@login_required
def inbox(request):
	player = Player.objects.get(user = request.user)
	messages = Message.objects.filter(recipent = player).order_by('-timestamp')
	print(messages)
	return render(request, 'game/inbox.html', {'player':player, 'unread_messages':count_messages(request), 'messages':messages})
	
@login_required
def view_message(request, mes):
	message = Message.objects.get(id = mes)
	player = Player.objects.get(user = request.user)
	if player == message.recipent or player == message.sender:
		if player == message.recipent:
			message.read = True
		message.save()
		return render(request, 'game/message.html', {'player':player, 'unread_messages':count_messages(request), 'message':message})
	else:
		return redirect('/messages/inbox/')

@login_required
def sent(request):
	player = Player.objects.get(user = request.user)
	messages = Message.objects.filter(sender = player).order_by('-timestamp')
	return render(request, 'game/sent.html', {'player':player, 'unread_messages':count_messages(request), 'messages':messages})

@login_required
def reply(request, mes):
	message = message = Message.objects.get(id = mes)
	player = Player.objects.get(user = request.user)
	if player == message.recipent or player == message.sender:
		if request.method == 'POST':
			form = MessageForm(request.POST)
			if form.is_valid():
				parser = get_parser()
				print(form.cleaned_data.get('recipent'))
				string = form.cleaned_data.get('recipent')
				user = User.objects.filter(username = string)
				if len(user) > 0:
					Message.objects.create(sender = player, recipent = Player.objects.filter(user=user)[0], subject = form.cleaned_data.get('subject'), content = (form.cleaned_data.get('message')), timestamp = datetime.utcnow().replace(tzinfo=utc))
				elif form.cleaned_data.get('recipent') == '[MM]':
					pass # TODO MM
				return redirect ('/messages/inbox/')
		else:
			text = '\n_____'+str(message.sender.user.username)+' wrote:_____\n'
			text += str(message.content)
			
			form = MessageForm(initial={'recipent':str(message.sender.user.username), 'subject':str(message.subject), 'message':text})
		return render(request, 'game/new_message.html', {'player':player, 'unread_messages':count_messages(request), 'form':form})
	else:
		return redirect('/messages/inbox/')
