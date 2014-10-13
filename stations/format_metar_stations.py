import sys
import os
import sqlite3

#http://weather.rap.ucar.edu/surface/stations.txt

#input_file_name = "C:\Users\jbarnett\Dropbox\Python\METAR\stations\test_stations.txt"

# Clear the screen so the junk is gone.
os.system('cls' if os.name == 'nt' else 'clear')

## Connect to the metar_stations database
conn = sqlite3.connect(r"metar_stations.db")
cursor = conn.cursor()


## Delete the records to allow for new records and compact the database
cursor.execute('DELETE FROM stations;')
cursor.execute("VACUUM") # Compact the database
conn.commit()

## Variables section
skip_header = "CD  S"
metar_station_yes = "X"
fix_count = 0

## Open the input file
#in_file_handle = open(r"C:\Users\jbarnett\Dropbox\Python\METAR\stations\test_stations.txt", "r")
#in_file_handle = open(r"C:\Users\jbarnett\Dropbox\Python\METAR\stations\short_test_stations.txt", "r")
#in_file_handle = open(r"C:\Users\jbarnett\Dropbox\Python\METAR\stations\stations.txt", "r")
in_file_handle = open(r"/Users/john/Dropbox/Python/METAR/stations/stations.txt", "r") #Mac
#in_file_handle = open(r"/Users/john/Dropbox/Python/METAR/stations/short_test_stations.txt", "r") #Mac
csv_header = "State,Station Description,ICAO,Country"
#Read the file

#out_file_handle = open(r"C:\Users\jbarnett\Dropbox\Python\METAR\stations\metar_stations.csv", "a")  #Windows
out_file_handle = open(r"/Users/john/Dropbox/Python/METAR/stations/metar_stations.csv", "a") #Mac
out_file_handle.write(csv_header + "\n")
#print(csv_header + "\n")


for line in in_file_handle:
	lenLine = len(line)
	csv_sep = ","
	m_fixedLine = line[62:63]
	#print(csv_header)
	
	#if line[0:5] == skip_header:  #This skips the page headers in the file
	if m_fixedLine != metar_station_yes:  
		skipped = line
	elif lenLine > 50:
		fix_count = fix_count + 1
		fixedLine = line[0:24]
		m_fixedLine = line[62:63]
		newFile_state = line[0:2] #1
		newFile_station = line[3:19] #2
		newFile_ICAO = line[20:24] #3
		newFile_IATA = line[26:29] #4
		newFile_SYNOP = line[32:37] #5
		newFile_LAT = line[39:45] #6
		newFile_LONG = line[47:54] #7
		newFile_ELEV = line[55:59] #8
		newFile_METAR = line[62:63] #9
		newFile_NEXRAD = line[65:66] #10
		newFile_AvFlag = line[68:69] #11
		newFile_UpperAir = line[71:72] #12
		newFile_Auto = line[74:75] #13
		newFile_OfficeType = line[77:78] #14
		newFile_PriPlot = line[79:80] #15
		newFile_Country = line[81:83] #16
		csv_new_line_a = newFile_state + csv_sep + newFile_station + csv_sep + newFile_ICAO + csv_sep + newFile_IATA + csv_sep + newFile_SYNOP + csv_sep + newFile_LAT + csv_sep + newFile_LONG + csv_sep + newFile_ELEV 
		csv_new_line_b = csv_sep + newFile_METAR + csv_sep + newFile_NEXRAD + csv_sep + newFile_AvFlag + csv_sep + newFile_UpperAir + csv_sep + newFile_Auto + csv_sep + newFile_OfficeType + csv_sep + newFile_PriPlot + csv_sep + newFile_Country
		csv_new_line = csv_new_line_a + csv_new_line_b
		db_string = (newFile_state, newFile_station, newFile_ICAO, newFile_IATA, newFile_SYNOP, newFile_LAT, newFile_LONG, newFile_ELEV, newFile_METAR, newFile_NEXRAD, newFile_AvFlag, newFile_UpperAir, newFile_Auto, newFile_OfficeType, newFile_PriPlot, newFile_Country)
		
		print(csv_new_line)
		#print(newFilePriPlot)
		
		#out_file_handle.write(csv_new_line + "\n")
		cursor.execute('INSERT INTO stations VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);',db_string)
	else:
		skipped = line  #Accommodates blank lines and other weird stuff 
		
	#out_file_handle.close()
print('\n'+ "Total lines processed: " + str(fix_count))
	
#read_out_file_handle = open(r"C:\Users\jbarnett\Dropbox\Python\METAR\stations\metar_stations_1.txt", "r")
#for line in read_out_file_handle:
#	print(line)
	
## Close the files	
in_file_handle.close()
cursor.execute("VACUUM") # Compact the database
conn.commit()
conn.close()
