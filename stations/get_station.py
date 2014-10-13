import sqlite3
import os

# Clear the screen so the junk is gone.
os.system('cls' if os.name == 'nt' else 'clear')

station_id = input('Please enter the ICAO station code: ')
#station_id = "kfSm"
station_id = station_id.upper()

metar_url = "http://w1.weather.gov/data/METAR/%s.1.txt" % station_id

print(metar_url)
## Connect to the metar_stations database
conn = sqlite3.connect(r"metar_stations.db")
cursor = conn.cursor()

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

print("\n\tfrom station " + station_id + " located in " + station_result + ", " + state_result + " (" + country_result + ")" )




