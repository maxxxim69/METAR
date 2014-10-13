import re

metar_line = "METAR KDFW 051953Z 13011G18KT 110V200 1/2SM SCT055 04/01  A3011 RMK AO2"
#print(metar_line)

metar_temp_regex = re.compile("M?\d\d\/M?\d\d")

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
	
