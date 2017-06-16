# -*- coding: utf-8 -*-

import datetime
from django.utils.timezone import utc
from django.conf import settings
import building
from models import *

def get_possible(player):
	buildings = ['pos_01', 'pos_02', 'pos_03', 'pos_04', 'pos_05', 'pos_06', 'pos_07', 'pos_08', 'pos_09', 'pos_10', 'pos_11', 'pos_12', 'pos_13', 'pos_14', 'pos_15', 'pos_16', 'pos_17', 'pos_18', 'pos_19', 'pos_20', 'pos_21', 'pos_22', 'pos_23', 'pos_24']
	village = player.last_village
	center = village.center
	
	bajte = []
	for building in buildings:
		bajta = getattr(center, building)
		try:
			bajte.append((bajta.building.name,bajta.lvl))
		except Exception:
			pass
			
	# Parliament, Summer residence = Headquarters >= 5
	# Town hall = Headquarters >= 10
	# Headquarters != Headquarters
	# Shelter = (! Shelter) || (Shelter == 10)
	# Warehouse, Silo, Bunker, Devensive line = Headquarters >= 1
	# University = Headquarters >= 5 && Training camp >= 3
	# Training camp = Headquarters  >= 3 && Bunker >= 1
	# Ammunition workshop =  University >= 1
	# Hangar, Port = University >= 5 && Ammunition workshop >= 3
	# Railway = Defensive line == 20
	# Artilery mansion = University >= 10
	# Hero's birth house = Bunker >= 1
	# Hideout = Headquarters >= 10 && University >= 5
	# Large warehouse, silo ## Later with artifacts
	# Large camp = Training camp == 20
	# Large hangar = Hangar == 20
	# Oil refinery
	# Iron works
	# Saw mill
	# Slaughter house
	# Can filling centre
	# Nuke research lab ## Nuke village only
	# Bazar = Market == 20
	# Market = Headwuarters == 3 && Warehouse, Silo >= 1
	
	# TODO production bonus
	fields = ['pos_01', 'pos_02', 'pos_03', 'pos_04', 'pos_05', 'pos_06', 'pos_07', 'pos_08', 'pos_09', 'pos_10', 'pos_11', 'pos_12', 'pos_13', 'pos_14', 'pos_15', 'pos_16', 'pos_17', 'pos_18']
	oil = False
	iron = False
	wood = False
	food1 = False
	food2 = False
	oilb = False
	ironb = False
	woodb = False
	food1b = False
	food2b = False
	for field in fields:
		polje = getattr(player.last_village.fields, field)
		if polje.lvl >= 10 and polje.name.name == 'Oil field':
			oil = True
		if polje.lvl >= 10 and polje.name.name == 'Iron mine':
			iron = True
		if polje.lvl >= 10 and polje.name.name == 'Forrest':
			wood = True
		if polje.lvl >= 10 and polje.name.name == 'Farm':
			food2 = True
		if polje.lvl >= 5 and polje.name.name == 'Farm':
			food1 = True
	buildings = ['Parliament','Summer residence' ,'Town hall' ,'Headquarters' ,'Shelter' ,'Warehouse' ,'Silo' ,'University','Market','Training camp','Ammunition workshop' ,'Hangar','Railway' ,'Port' ,'Artilery mansion' ,"Hero's birth house",'Hideout' ,'Large warehouse','Large silo','Large camp','Large hangar','Bunker','Defensive line','Oil refinery','Iron works','Sawmill' ,'Slaughter house' ,'Can filling centre','Nuke research lab','Bazar']
	possible = []
	for bajta in bajte:
		if bajta[0] == 'Oil refinery':
			oilb = True
		if bajta[0] == 'Iron works':
			ironb = True
		if bajta[0] == 'Sawmill':
			woodb = True
		if bajta[0] == 'Slaughter house':
			food1b = True
			food1blvl = bajta[1]
		if bajta[0] == 'Can filling centre':
			foodb2 = True
		if bajta[0] == 'Headquarters' and bajta[1] >= 5:
			ok = True
			for kuca in bajte:
				if kuca[0] == 'Parliament' or kuca[0] == 'Summer residence':
					ok = False
			if ok:
				if not player.parliament:
					possible.append('Parliament')
				possible.append('Summer residence')
			
			for kuca in bajte:
				if kuca[0] == 'Training camp' and kuca[1] >= 3:
					ok = True
					for house in bajte:
						if house[0] == 'University':
							ok = False
					if ok:
						possible.append('University')
						
		if bajta[0] == 'Headquarters' and bajta[1] >= 1:
			ok = True
			for kuca in bajte:
				if kuca[0] == 'Warehouse' and kuca[1] < 20:
					ok = False
			if ok:
				possible.append('Warehouse')
			
			ok = True
			for kuca in bajte:
				if kuca[0] == 'Silo' and kuca[1] < 20:
					ok = False
			if ok:
				possible.append('Silo')
			
			ok = True
			for kuca in bajte:
				if kuca[0] == 'Bunker':
					ok = False
			if ok:
				possible.append('Bunker')
			
			ok = True
			for kuca in bajte:
				if kuca[0] == 'Defensive line':
					ok = False
			if ok:
				possible.append('Defensive line')
				

			
		if bajta[0] == 'Headquarters' and bajta[1] >= 3:
			for kuca in bajte:
				if kuca[0] == 'Bunker' and kuca[1] >= 1:
					ok = True
					for house in bajte:
						if house[0] == 'Training camp':
							ok = False
					if ok:
						possible.append('Training camp')
			
			okw = False
			oks = False	
			ok = True		
			for kuca in bajte:
				if kuca[0] == 'Warehouse':
					okw = True
				if kuca[0] == 'Silo':
					oks = True
				if kuca[0] == 'Market':
					ok = False
			
			if okw and oks and ok:
				possible.append('Market')			
						
		if bajta[0] == 'University':
			ok = True
			for kuca in bajte:
				if kuca[0] == 'Ammunition workshop':
					ok = False
			
			if ok:
				possible.append('Ammunition workshop')
				
		if bajta[0] == 'Defensive line' and bajta[1] == 20:
			ok = True
			for kuca in bajte:
				if kuca[0] == 'Railway':
					ok = False
			
			if ok:
				possible.append('Railway')
				
		if bajta[0] == 'University' and bajta[1] >= 5:
			for kuca in bajte:
				if kuca[0] == 'Ammunition workshop' and kuca[1] >= 3:
					
					ok = True
					for i in bajte:
						if i[0] == 'Hangar':
							ok = False
							
					if ok:
						possible.append('Hangar')
						
					ok = True
					for i in bajte:
						if i[0] == 'Port':
							ok = False
							
					if ok:
						possible.append('Port')
		
		if bajta[0] == 'University' and bajta[1] >= 10:
			ok = True
			for i in bajte:
				if i[0] == 'Artilery mansion':
					ok = False
					
			if ok:
				possible.append('Artilery mansion')
				
		if bajta[0] == 'Bunker' and bajta[1] >= 1:
			ok = True
			for i in bajte:
				if i[0] == "Hero's birth house":
					ok = False
					
			if ok:
				possible.append("Hero's birth house")
				
		if bajta[0] == 'Headquarters' and bajta[1] >= 10:
			for kuca in bajte:
				if kuca[0] == 'University' and kuca[1] >= 5:
					ok = True
					for i in bajte:
						if i[0] == 'Hideout':
							ok = False
					
					if ok:
						possible.append('Hideout')
						
		if bajta[0] == 'Training camp' and bajta[1] == 20:
			ok = True
			for i in bajte:
				if i[0] == 'Large camp':
					ok = False
					
			if ok:
				possible.append('Large camp')
				
		if bajta[0] == 'Hangar' and bajta[1] == 20:
			ok = True
			for i in bajte:
				if i[0] == 'Large hangar':
					ok = False
					
			if ok:
				possible.append('Large hangar')
				
		if bajta[0] == 'Market' and bajta[1] == 20:
			ok = True
			for i in bajte:
				if i[0] == 'Bazar':
					ok = False
			
			if ok:
				possible.append('Bazar')
				
	ok = True
	for kuca in bajte:
		if kuca[0] == 'Shelter' and kuca[1] < 10:
			ok = False
	if ok:
		possible.append('Shelter')
		
	if oil and not oilb:
		possible.append('Oil refinery')
		
	if iron and not ironb:
		possible.append('Iron works')
		
	if wood and not woobd:
		possible.append('Sawmill')
		
	if food1 and not food1b:
		possible.append('Slaughter house')
		
	if food2 and not food2 and food1blvl == 5:
		possible.append('Can filling centre')
	
	return possible
