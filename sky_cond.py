import re
import sys

#full_metar_line = "METAR KFSM 050253Z 11004G02KT 10SM SKC 25/18 A3018 RMK AO2 SLP216 T02500183 53003" #CLR
#full_metar_line = "METAR KFSM 050253Z 11004G02KT 10SM CLR 25/18 A3018 RMK AO2 SLP216 T02500183 53003" #CLR
#full_metar_line = "METAR KDFW 051953Z 13011G18KT 110V200 10SM SCT015TCU 33/20 A3011 RMK AO2" #SCT
#full_metar_line = "METAR KDFW 061353Z 21010KT 10SM BKN250 28/21 A3006 RMK AO2 SLP170" #BKN
#full_metar_line = "METAR KDFW 061353Z 21010KT 10SM OVC250 28/21 A3006 RMK AO2 SLP170" #OVC
#full_metar_line = "METAR KDFW 061353Z 21010KT 10SM FEW999 28/21 A3006 RMK AO2 SLP170" #FEW
#full_metar_line = "METAR KDFW 061353Z 21010KT 10SM VV250 28/21 A3006 RMK AO2 SLP170" #Vertical visibility
#full_metar_line = "METAR KDFW 061353Z 21010KT 10SM CAVOK 28/21 A3006 RMK AO2 SLP170" #CAVOK
#full_metar_line = "METAR KDFW 061353Z 21010KT 10SM 28/21 A3006 RMK AO2 SLP170" #No sky info
full_metar_line = "METAR KDFW 071953Z 18010KT 10SM SCT065TCU BKN090 BKN250 36/19 A2993 RMK" #more than one sky condition


## Trim off the remarks section
metar_line = full_metar_line.split("RMK")[0]
print(metar_line)

metar_sky_cond_regex = re.compile("CAVOK|CLR|SKC|SCT\d\d\d|FEW\d\d\d|BKN\d\d\d|OVC\d\d\d|VV\d\d\d")

try:
	find_sky_cond = metar_sky_cond_regex.findall(metar_line)
	print("Current Sky Conditions:")
	for index in range(len(find_sky_cond)):
		metar_sky_cond = find_sky_cond[index]
		len_metar_sky_cond = len(metar_sky_cond)
		if len_metar_sky_cond == 3:
			metar_sky_contraction = metar_sky_cond
			print("Clear skies, unlimited visibility")
		elif len_metar_sky_cond == 5:
			if metar_sky_cond == "CAVOK":
				print("Clear skies, unlimited visibility")
			else:
				print("Vertical visibility for obscuration. Maybe foggy.")
		elif len_metar_sky_cond == 6:
			metar_sky_contraction = metar_sky_cond[0:3]
			metar_ht_base = metar_sky_cond[3:6]
			metar_height = int(metar_ht_base)*100
			if metar_sky_contraction == "SCT":
				print("Scattered clouds with height of the base at " + str(metar_height) + " feet")
			elif metar_sky_contraction == "FEW":
				print("A few clouds with height of the base at " + str(metar_height) + " feet")
			elif metar_sky_contraction == "BKN":
				print("Broken clouds with height of the base at " + str(metar_height) + " feet")
			elif metar_sky_contraction == "OVC":
				print("Overcast skies with height of the base at " + str(metar_height) + " feet")
			#print(metar_sky_contraction)
			#print(metar_ht_base)
			#print(str(metar_height))
		else:
			print("There is an issue with sky conditions")
except IndexError as detail:
	print("Sky condition information is not present in the information file.")
	

	

