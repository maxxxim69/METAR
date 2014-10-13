# http://w1.weather.gov/data/METAR/KFSM.1.txt
# http://www.wunderground.com/metarFAQ.asp
# http://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3
# http://weather.noaa.gov/pub/data/observations/metar/



import urllib.request
import shutil

# METAR download URL and output file name
metar_url = "http://w1.weather.gov/data/METAR/KFSM.1.txt"
file_name = "kfsm.txt"

# Download the file from `metar_url` and save it locally under `file_name`:
with urllib.request.urlopen(metar_url) as response, open(file_name, 'wb') as out_file:
	shutil.copyfileobj(response, out_file)
	

metar_line = open(file_name, "r").readlines()[3]

#          1         2         3         4         5         6
#01234567890123456789012345678901234567890123456789012345678901234
#METAR KFSM 020053Z 33006KT 10SM FEW050 32/22 A2987 RMK AO2 SLP108

metar_header = metar_line[0:5]
metar_station_id = metar_line[6:10]
metar_time = metar_line[11:18]
metar_winds_degree = metar_line[19:22]
metar_winds_speed = metar_line[22:24]
metar_visibility = metar_line[27:29]
metar_sky_cover = metar_line[32:35]
metar_present_weather = metar_line[32:38]
metar_temp_celsius = metar_line[39:41]
metar_temp_dew_point_celsius = metar_line[42:44]

#metar_temp_fahrenheit = float(metar_temp_celsius) * 1.8 + 32
#metar_temp_dew_point_fahrenheit = float(metar_temp_dew_point_celsius) * 1.8 + 32

print(metar_temp_dew_point_celsius)
print(metar_temp_dew_point_celsius)



print('\n' + metar_line + '\n')

#print("Header: " + metar_header) #METAR
print('\n'+"Station: " + metar_station_id) #Station
print("Zulu Time: " + metar_time) #METAR Time (UTC)
print("Winds direction: " + metar_winds_degree + " degrees") #METAR Winds Degree
print("Winds speed: " + metar_winds_speed + " knots") #METAR Winds Speed
print("Visibility: " + metar_visibility + " statute mile(s)") #METAR Visibility in Statute Miles
print("Sky cover: " + metar_sky_cover) #METAR Sky Cover
print("Present Weather and Obscurations: " + metar_present_weather) #METAR Present Weather and Obscurations
print("Temperature: " + str(metar_temp_fahrenheit)+ "F " + "(" + metar_temp_celsius + "C" +")") #METAR Temperature


print("Dew Point: " + str(metar_temp_dew_point_fahrenheit)+ "F " + "(" + metar_temp_dew_point_celsius + "C" + ")") #METAR Dew Point Temp in Celsius

print('\n')
