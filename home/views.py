# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import RequestContext
from django.shortcuts import render
from django.shortcuts import render_to_response

# Create your views here.

def index(request):
	return render_to_response('home/index.html')
	
def about(request):
	return render_to_response('home/about.html')
	
def tutorial(request):
	return render_to_response('home/tutorial.html')
	
def developers(request):
	return render_to_response('home/developers.html')
	
def pricing(request):
	return render_to_response('home/pricing.html')
	
def sponsors(request):
	return render_to_response('home/sponsors.html')
	
def private(request):
	return render_to_response('home/private.html')

	
	
