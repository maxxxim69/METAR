import sqlite3

# Create the database and open a cursor for the db
conn = sqlite3.connect(r"metar_stations.db") # or use :memory: to put it in RAM
cursor = conn.cursor()

# Create tables

# Create stations
cursor.execute('''CREATE TABLE stations (State text, Station text, ICAO text, IATA text, SYNOP text, LAT text, LONG text, ELEV text, METAR text, NEXRAD text, AvFlag text, UpperAir text, Auto text, OfficeType text, PriPlot text, Country text)''')

# Program maintenance table with default values
#cursor.execute('''CREATE TABLE maint_parms (db_ver real, db_locked integer)''')
#cursor.execute('INSERT INTO maint_parms VALUES (1.0,0);')

# Database clean up commands
conn.commit()
conn.close()


