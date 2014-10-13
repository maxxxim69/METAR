# http://w1.weather.gov/data/METAR/KFSM.1.txt
# http://www.wunderground.com/metarFAQ.asp
# http://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3
# http://weather.noaa.gov/pub/data/observations/metar/

#   CD = 2 letter state (province) abbreviation
#   STATION = 16 character station long name
#   ICAO = 4-character international id
#   IATA = 3-character (FAA) id
#   SYNOP = 5-digit international synoptic number
#   LAT = Latitude (degrees minutes)
#   LON = Longitude (degree minutes)
#   ELEV = Station elevation (meters)
#   M = METAR reporting station.   Also Z=obsolete? site
#   N = NEXRAD (WSR-88D) Radar site
#   V = Aviation-specific flag (V=AIRMET/SIGMET end point, A=ARTCC T=TAF U=T+V)
#   U = Upper air (rawinsonde=X) or Wind Profiler (W) site
#   A = Auto (A=ASOS, W=AWOS, M=Meso, H=Human, G=Augmented) (H/G not yet impl.)
#   C = Office type F=WFO/R=RFC/C=NCEP Center
#   Digit that follows is a priority for plotting (0=highest)
#   Country code (2-char) is last column


import urllib.request
import shutil
import time
import os
import datetime
import re
import sqlite3

#Fix the following, see lines below...
#	1. Variable wind speeds
# 	2. Correct this time to match timezone

## Connect to the metar_stations database
conn = sqlite3.connect(r"metar_stations.db")
cursor = conn.cursor()

# Clear the screen so the junk is gone.
os.system('cls' if os.name == 'nt' else 'clear')

station_id = input('Please enter the ICAO station code: ')
station_id = station_id.upper() #fix the ICAO to all upper-case for the query

## Get station information from database
try:
## Get the state of the station
	sql_state = "SELECT state FROM stations WHERE ICAO =?;"
	cursor.execute(sql_state, [(station_id)])
	state_result = ([(theRecord[0]) for theRecord in cursor.fetchall()])
	state_result = state_result[0]

	## Get the station description
	sql_station_desc = "SELECT station FROM stations WHERE ICAO =?;"
	cursor.execute(sql_station_desc, [(station_id)])
	station_result = ([(theRecord[0]) for theRecord in cursor.fetchall()])
	station_result = station_result[0]
	station_result = station_result.strip()
	station_result = station_result.title()

	## Get the station country
	sql_station_desc = "SELECT country FROM stations WHERE ICAO =?;"
	cursor.execute(sql_station_desc, [(station_id)])
	country_result = ([(theRecord[0]) for theRecord in cursor.fetchall()])
	country_result = country_result[0]

	station_info = " from station " + station_id + " located in " + station_result + ", " + state_result + " (" + country_result + ")"
except IndexError as detail:
	print("The IACO code is not valid.")
	is_an_error = True
	exit()

# METAR download URL and output file name
metar_url = "http://w1.weather.gov/data/METAR/%s.1.txt" % station_id
#metar_url = "http://w1.weather.gov/data/METAR/KDFW.1.txt" #Dallas, TX
#metar_url = "http://w1.weather.gov/data/METAR/KFSM.1.txt" #Fort Smith, AR
#metar_url = "http://w1.weather.gov/data/METAR/KLIT.1.txt" #Little Rock, AR
file_name = "metar_output.txt"
is_an_error = False

# Download the file from `metar_url` and save it locally under `file_name`:
with urllib.request.urlopen(metar_url) as response, open(file_name, 'wb') as out_file:
	shutil.copyfileobj(response, out_file)

## Read the 4th line and turn it into a list
## it should return something like:  METAR KFSM 021353Z 25004KT 10SM CLR 25/18 A3005 RMK AO2 SLP168
full_metar_line = open(file_name, "r").readlines()[3]
"""
#full_metar_line = "METAR KFSM 050253Z 11004G02KT 10SM CLR 25/18 A3018 RMK AO2 SLP216 T02500183 53003"
#full_metar_line = "METAR KDFW 051953Z 13011G18KT 110V200 10SM SCT055 33/20 A3011 RMK AO2" #Wind gusts
#full_metar_line = "METAR KDFW 061353Z 21010KT 10SM BKN250 28/21 A3006 RMK AO2 SLP170" 
#full_metar_line = "SPECI KFSM 050253Z 11004KT 10SM CLR 25/18 A3018 RMK AO2 SLP216 T02500183 53003"
#full_metar_line = "METAR KDEN 072053Z 29014G20KT 10SM SCT090 SCT150 SCT200 38/M01 A3001 RMK" #2. Neg Temps
#full_metar_line = "METAR KLAS 072056Z VRB03KT 10SM FEW080 BKN150 BKN200 37/11 A2986 RMK AO2" #1. Variable wind speed
#full_metar_line = "METAR KLIT 090153Z 32012G22KT 2SM +TSRA FEW010 SCT025 OVC042CB 22/19 A3001 RMK AO2 PK WND 33037/0127 WSHFT 0113 TSB04RAB18 SLP161 FRQ LTGICCG ALQDS TS ALQDS MOV SE P0013 T02170189"
#full_metar_line = "SPECI KMEM 090202Z 29021G31KT 3SM +TSRA SCT023 BKN033CB OVC095 24/22 A2995 RMK AO2 PK WND 30031/0201 WSHFT 0146 CONS LTGICCG ALQDS TS ALQDS MOV E P0003"
#print(full_metar_line)"""

## Trim off the remarks section
metar_line = full_metar_line.split("RMK")[0]
#print(metar_line + '\n')

## Build the regular expression values
metar_type_regex = re.compile("METAR|SPECI")
metar_station_id_regex = re.compile("K\w\w\w|\sP\w\w\w|C\w\w\w")
metar_temp_regex = re.compile("M?\d\d\/M?\d\d")
metar_date_time = re.compile("\d\d\d\d\d\dZ")
metar_wind_regex = re.compile("\d\d\d\d\dG?\d?\d?KT|VRB\d\dKT")
metar_visibility_regex = re.compile("\d\d?SM|M?\d\/\dSM|1\s\d\/\dSM")
#metar_clouds_regext = re.compile("[A-Z][A-Z][A-Z][0-9][0-9][0-9]|\s[A-Z][A-Z][A-Z]\s")
metar_sky_cond_regex = re.compile("CAVOK|CLR|SKC|SCT\d\d\d|FEW\d\d\d|BKN\d\d\d|OVC\d\d\d|VV\d\d\d")
metar_altimeter_regex = re.compile("A\d\d\d\d")
	

## Find and Parse the METAR report type
try:
	find_metar_type = metar_type_regex.findall(metar_line)
	metar_type = find_metar_type[0]
	if metar_type == "METAR":
		report_is = "Scheduled observation"
		#print("Scheduled observation")
	elif metar_type == "SPECI":
		report_is = "Unscheduled observation"
		#print("Unscheduled observation")
except IndexError as detail:
	print("Malformed report, no report type in file. Program terminated!")
	is_an_error = True
	print(metar_line + '\n')
	exit()

## Find and Parse the METAR Station ID
try:
	find_metar_station_id = metar_station_id_regex.findall(metar_line)
	metar_station_id = find_metar_station_id[0]
except IndexError as detail:
	print("Malformed report, no station id in file. Program terminated!")
	is_an_error = True
	print(metar_line + '\n')
	exit()


## Find and parse the date and time of the reading
try:
	find_date_time = metar_date_time.findall(metar_line)
	metar_date_time = find_date_time[0]
	metar_date_time_day = metar_date_time[0:2]
	metar_date_time_time_hour = metar_date_time[2:4]
	metar_date_time_time_min = metar_date_time[4:6]

	print('\n' + report_is + " readings from the " + metar_date_time_day + " day of the month at " + metar_date_time_time_hour+":"+ metar_date_time_time_min + " zulu" + station_info + '\n')
except IndexError as detail:
	print("Malformed report, no date or time in file. Program terminated!")
	is_an_error = True
	print(metar_line + '\n')
	exit()


## Find and parse the temperature and dew point in the file
try:
	find_temp_str = metar_temp_regex.findall(metar_line)
	metar_temps = find_temp_str[0]
	len_metar_temps = len(metar_temps)
	metar_temps_split = metar_temps.split("/")
	metar_temp_c =  metar_temps_split[0]
	metar_dew_pt_c = metar_temps_split[1]
	len_metar_temp_c = len(metar_temp_c)
	len_metar_dew_pt_c = len(metar_dew_pt_c)

	if len_metar_temp_c == 3:
		metar_temp_c = int(metar_temp_c[1:3])
		metar_temp_c = metar_temp_c * -1
		metar_temp_f = round(float(metar_temp_c * 1.8 + 32),2)
	elif len_metar_temp_c == 2:
		metar_temp_c = int(metar_temp_c)
		metar_temp_f = round(float(metar_temp_c * 1.8 + 32),2)
	else:
		print("temp something is wrong")

	if len_metar_dew_pt_c == 3:
		metar_dew_pt_c = int(metar_dew_pt_c[1:3])
		metar_dew_pt_c = metar_dew_pt_c * -1
		metar_dew_pt_f = round(float(metar_dew_pt_c * 1.8 + 32),2)
	elif len_metar_dew_pt_c == 2:
		metar_dew_pt_c = int(metar_dew_pt_c)
		metar_dew_pt_f = round(float(metar_dew_pt_c * 1.8 + 32),2)
	else:
		print("dew point something is wrong")
		
	print("Temperatures and Wind Information:")
	print("\tTemperature at reading: " + str(metar_temp_f) + "F or " + str(metar_temp_c) + "C")
	print("\tDew Point at reading: " + str(metar_dew_pt_f) + "F or " + str(metar_dew_pt_c) + "C")

except IndexError as detail:
	print("No Temperature information is present in the file.\n")
	is_an_error = True

try:	
	## Find and parse the wind direction and speed in the file
	find_wind = metar_wind_regex.findall(metar_line)
	metar_wind = find_wind[0]
	len_metar_wind = len(metar_wind)

	if len_metar_wind == 7:
		metar_wind_dir = metar_wind[0:3]
		metar_wind_speed = metar_wind[3:5]
		print("\tWind direction: " + metar_wind_dir + " degrees")
		print("\tWind speed: " + metar_wind_speed + " knots")
		#print(metar_wind)
	elif len_metar_wind ==10:
		metar_wind_dir = metar_wind[0:3]
		metar_wind_speed = metar_wind[3:5]
		metar_wind_gust = metar_wind[6:8]
		print("\tWind direction: " + metar_wind_dir + " degrees")
		print("\tWind speed: " + metar_wind_speed + " knots")
		print("\tWind gusting at: " + metar_wind_gust + " knots\n")
		#print(metar_wind)
	else:
		print("there is an issue with wind and speed")
		
except IndexError as detail:
	print("\n\tNo wind information is present in the file.\n")
	is_an_error = True


## Sky conditions
try:
	find_sky_cond = metar_sky_cond_regex.findall(metar_line)
	print("\nCurrent Sky Conditions:")
	for index in range(len(find_sky_cond)):
		metar_sky_cond = find_sky_cond[index]
		len_metar_sky_cond = len(metar_sky_cond)
		if len_metar_sky_cond == 3:
			metar_sky_contraction = metar_sky_cond
			print("\tClear skies, unlimited visibility")
		elif len_metar_sky_cond == 5:
			if metar_sky_cond == "CAVOK":
				print("\tClear skies, unlimited visibility")
			else:
				print("\tVertical visibility for obscuration. Maybe foggy?")
		elif len_metar_sky_cond == 6:
			metar_sky_contraction = metar_sky_cond[0:3]
			metar_ht_base = metar_sky_cond[3:6]
			metar_height = int(metar_ht_base)*100
			if metar_sky_contraction == "SCT":
				print("\tScattered clouds with height of the base at " + str(metar_height) + " feet")
			elif metar_sky_contraction == "FEW":
				print("\tA few clouds with height of the base at " + str(metar_height) + " feet")
			elif metar_sky_contraction == "BKN":
				print("\tBroken clouds with height of the base at " + str(metar_height) + " feet")
			elif metar_sky_contraction == "OVC":
				print("\tOvercast skies with height of the base at " + str(metar_height) + " feet")
			#print(metar_sky_contraction)
			#print(metar_ht_base)
			#print(str(metar_height))
		else:
			print("There is an issue with sky conditions")
except IndexError as detail:
	print("Sky condition information is not present in the information file.")
	is_an_error = True
	#print(metar_line)

	
## Find and parse altimeter settings
try:
	find_altimeter = metar_altimeter_regex.findall(metar_line)
	metar_altimeter_full = find_altimeter[0]
	metar_altimeter = metar_altimeter_full[1:5]
	metar_altimeter_Hg = round(int(metar_altimeter) * .01,2)
	print("\nAltimeter setting: " + str(metar_altimeter_Hg) + " Hg")
except IndexError as detail_alt:
	print("\nAltimeter information is not present in the information file.")
	is_an_error = True
	#print(metar_line)


## Find and parse the visibility information in the file
try:
	find_visibility = metar_visibility_regex.findall(metar_line)
	metar_visibility = find_visibility[0]
	len_metar_visibility = len(metar_visibility)
	#print(metar_visibility)
	#print(str(len_metar_visibility))
	if len_metar_visibility == 3:
		report_metar_visibility = metar_visibility[0:1]
		print("Reported visibility: "  + report_metar_visibility + " statue miles")
	elif len_metar_visibility == 4:
		report_metar_visibility = metar_visibility[0:2]
		print("Reported visibility: "  + report_metar_visibility + " statue miles")
	elif len_metar_visibility == 5:
		report_metar_visibility = metar_visibility[0:3]
		print("Reported visibility: "  + report_metar_visibility + " statue mile")
	elif len_metar_visibility == 6:
		report_metar_visibility = metar_visibility[1:4]
		print("Reported visibility: Less than "  + report_metar_visibility + " statue mile")
	elif len_metar_visibility == 7:
		report_metar_visibility = metar_visibility[0:5]
		print("Reported visibility: "  + report_metar_visibility + " statue miles")
	else:
		print("Error reporting visibility information.")
except IndexError as detail_alt:
	print("\nVisibility information is not present in the information file.")
	is_an_error = True
	#print(metar_line)


## This is the end of the program
print('\n')

if is_an_error == True:
	print("Error in the file.  Files METAR contains the following:")
	print(metar_line)
	#print(full_metar_line)

exit()