import re

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

metar_altimeter_regex = re.compile("A\d\d\d\d")
## Find and parse altimeter settings
find_altimeter = metar_altimeter_regex.findall(metar_line)
metar_altimeter_full = find_altimeter[0]
#print(metar_altimeter_full)
metar_altimeter = metar_altimeter_full[1:5]
#print(metar_altimeter)
metar_altimeter_Hg = int(metar_altimeter) * .01
print("Altimeter setting: " + str(metar_altimeter_Hg) + " Hg")

