import csv

with open('town-hall.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in spamreader:
		fields = row[0].split(',')
		print fields
