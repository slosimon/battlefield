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
from django.http import JsonResponse
from slugify import slugify

def count_messages(request):
	player = Player.objects.get(user = request.user)
	return len(Message.objects.filter(read = False, recipent = player))

def invitations(request):
	player = Player.objects.get(user = request.user)
	total = len(Invitation.objects.filter(invited = player))
	response_data ={}
	response_data['invitations'] = total
	response_data['gold'] = player.gold
	print(len(Message.objects.filter(read = False, recipent = player)))
	response_data['messages_count'] = count_messages(request)
	print(response_data)
	return (response_data)
