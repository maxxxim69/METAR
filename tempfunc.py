def relhumidity(temp_c, dewpt_c, round_num):
	
	e_const = 2.71828182845904	
	
	numerator_1 = (17.625*dewpt_c)/(243.04+dewpt_c)
	denominator_1 = (17.625*temp_c)/(243.04+temp_c)
	
	numerator_2 = e_const ** numerator_1
	denominator_2 = e_const ** denominator_1
	
	relativeHumidity  = (numerator_2 / denominator_2) * 100
	
	return round(relativeHumidity,round_num)

