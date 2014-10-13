import re

#metar_line = "METAR KDFW 051953Z 13011G18KT 110V200 M1/4SM SCT055 33/20 A3011 RMK AO2" #Y len=6
#metar_line = "METAR KDFW 051953Z 13011G18KT 110V200 1/2SM SCT055 33/20 A3011 RMK AO2" #Y len=5
metar_line = "METAR KDFW 051953Z 13011G18KT 110V200 1 1/2SM SCT055 33/20 A3011 RMK AO2" #Y len=7
#metar_line = "METAR KDFW 051953Z 13011G18KT 110V200 10SM SCT055 33/20 A3011 RMK AO2" #Y len=4
print(metar_line)

metar_visibility_regex = re.compile("\d\dSM|M?\d\/\dSM|1\s\d\/\dSM")

## Find and parse the visibility information in the file

try:
	find_visibility = metar_visibility_regex.findall(metar_line)
	metar_visibility = find_visibility[0]
	len_metar_visibility = len(metar_visibility)
	#print(metar_visibility)
	#print(str(len_metar_visibility))
	if len_metar_visibility == 4:
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
	print(metar_line)