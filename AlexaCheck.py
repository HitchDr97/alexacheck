import cStringIO
from urllib import urlopen
import json
import os.path
import zipfile
import time
from datetime import datetime



ALEXA_DATA_URL = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'

def write_config():
	a = datetime.now().time()
	print a.isoformat()
	file = open("alexasites.config", "w")
	file.write(a.isoformat())

	file.close()
	print("The config file has been written!")
def download_and_save():

	f = urlopen(ALEXA_DATA_URL)

	buf = cStringIO.StringIO(f.read())

	zfile = zipfile.ZipFile(buf)

	buf = cStringIO.StringIO(zfile.read('top-1m.csv'))
	url_dict = {}

	for item in buf:
		(rank, domain) = item.split(',')
		domain_clean = domain.rstrip()
		url_dict[domain_clean] = rank



	with open('alexasites.json', 'w') as outfile:
		json.dump(url_dict, outfile)
	print("The data has been downloaded and saved!")

def start(myDomain):

	#alexasites.json file exists
	data_file_path = "alexasites.json"
	config_file_path = "alexasites.config"
	if os.path.isfile(data_file_path) == True and os.path.isfile(config_file_path)== True: #See if config and json exist

		file = open("alexasites.config", "r")
		last_save = file.read()

	#If the age is older than 10 minutes
		b = datetime.now()
		b = b.time()

		fmt = "%H:%M:%S.%f"
		c = datetime.strptime(b.isoformat(), fmt) - datetime.strptime(last_save, fmt)
		if c.days < 0: #Hack in case midnight occurred since last update, may not be necessary
			c = timedelta(days=0,seconds=c.seconds,microseconds=c.microseconds)
		minutes_since = (c.seconds/60)#divide seconds since by 60 to convert to minutes
		if minutes_since > 10:

			write_config()
			download_and_save()
			read_json(myDomain)
		else:

			read_json(myDomain)
	else: #Write a new config file and download new data

		write_config()
		download_and_save()
		read_json(myDomain)



def read_json(domain):
    # Read the json file into a variable
	d ={}
	with open('alexasites.json') as json_data:
		d = json.load(json_data)
	try:
		print domain+ "'s rank is "+ d[domain]
	except KeyError:
		print "This URL is not in the Alexa Top Million"




	#Check if myDomain exists within the list of dictionaries
	#If exists:
		#Print exists
		#Print rank
	#Else:
		#Print it doesn't exist

userinput=""
while not userinput == "exit":
	userinput = raw_input("What domain do you want to search for: ")
	if not userinput == "":
		start(userinput)
	else:
		print "Enter something this time"