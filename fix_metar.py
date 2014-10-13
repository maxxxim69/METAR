import urllib.request
import shutil
import time
import os
import datetime
import re

#
# 


# Clear the screen so the junk is gone.
os.system('cls' if os.name == 'nt' else 'clear')

# METAR download URL and output file name
#metar_url = "http://w1.weather.gov/data/METAR/KDFW.1.txt"
metar_url = "http://w1.weather.gov/data/METAR/KFSM.1.txt"
file_name = "metar_output.txt"

# Download the file from `metar_url` and save it locally under `file_name`:
with urllib.request.urlopen(metar_url) as response, open(file_name, 'wb') as out_file:
	shutil.copyfileobj(response, out_file)

## Read the 4th line and turn it into a list
## it should return something like:  METAR KFSM 021353Z 25004KT 10SM CLR 25/18 A3005 RMK AO2 SLP168
full_metar_line = open(file_name, "r").readlines()[3]
#full_metar_line = "METAR KFSM 050253Z 11004G02KT 10SM CLR 25/18 A3018 RMK AO2 SLP216 T02500183 53003"
#full_metar_line = "METAR KDFW 051953Z 13011G18KT 110V200 10SM SCT055 33/20 A3011 RMK AO2"
#full_metar_line = "METAR KDFW 061353Z 21010KT 10SM BKN250 28/21 A3006 RMK AO2 SLP170"
print(full_metar_line)

metar_line = full_metar_line.split("RMK")[0]
print(metar_line)