# http://w1.weather.gov/data/METAR/KFSM.1.txt
# http://www.wunderground.com/metarFAQ.asp
# http://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3
# http://weather.noaa.gov/pub/data/observations/metar/

import urllib.request
import shutil
import time
import os
import datetime

# Clear the screen so the junk is gone.
os.system('cls' if os.name == 'nt' else 'clear')

# METAR download URL and output file name
#metar_url = "http://w1.weather.gov/data/METAR/KMSP.1.txt"
metar_url = "http://w1.weather.gov/data/METAR/KFSM.1.txt"
file_name = "kfsm.txt"

# Download the file from `metar_url` and save it locally under `file_name`:
with urllib.request.urlopen(metar_url) as response, open(file_name, 'wb') as out_file:
	shutil.copyfileobj(response, out_file)

## Read the 4th line and turn it into a list
## it should return something like:  METAR KFSM 021353Z 25004KT 10SM CLR 25/18 A3005 RMK AO2 SLP168
metar_line = open(file_name, "r").readlines()[3]
metar_line_list = metar_line.split()

##  0     1     2       3      4   5    6     7    8   9    10
##METAR KFSM 021353Z 25004KT 10SM CLR 24/21 A3005 RMK AO2 SLP168

## Some debugging code here
print(metar_line)

#for index in range(len(metar_line_list)):
#   print(metar_line_list[index])

## Assign the station id to a variable
metar_station_id = metar_line_list[1]

## Parse and convert the date section of the output
metar_reading = metar_line_list[2]
metar_reading_day = metar_reading[0:2]
metar_reading_time_hour = metar_reading[2:4]
metar_reading_time_min = metar_reading[4:6]
metar_reading_time = metar_reading_time_hour +":" + metar_reading_time_min
converted_metar_time = datetime.time(int(metar_reading_time_hour), int(metar_reading_time_min), 0, tzinfo=None)
print(str(converted_metar_time))


print('\n'+"Readings from the " + metar_reading_day + " day of the month at " + metar_reading_time + " zulu from station " + metar_station_id)

## Parse and convert the Temperature section of the output
metar_temps = metar_line_list[6]
metar_temp_celsius = metar_temps[0:2]
metar_dew_point_celsius = metar_temps[3:5]

metar_temp_fahrenheit = str(round(float(metar_temp_celsius) * 1.8 + 32,2))
metar_dew_point_fahrenheit = str(round(float(metar_dew_point_celsius) * 1.8 + 32,2))

print('\n'+"Temperature: " + metar_temp_celsius + "C" + " or " + metar_temp_fahrenheit + "F")
print("Dew Point: " + metar_dew_point_celsius + "C" + " or " + metar_dew_point_fahrenheit + "F"+'\n')






