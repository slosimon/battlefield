import csv
from slugify import slugify
buildings = ['Parliament','Summer residence' ,'Town hall' ,'Headquarters' ,'Shelter' ,'Warehouse' ,'Silo' ,'University','Market','Training camp','Ammunition workshop' ,'Hangar','Railway' ,'Port' ,'Artilery mansion' ,"Hero's birth house",'Hideout' ,'Large warehouse','Large silo','Large camp','Large hangar','Bunker','Defensive line','Oil refinery','Iron works','Sawmill' ,'Slaughter house' ,'Can filling centre','Nuke research lab','Bazar']
for build in buildings:
	print(slugify(str(build)))
	#print(str('init/'+slugify(str(build))+'.csv'))


