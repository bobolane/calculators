from nec_tables_vd import NECTables

class FinalCalc(object):
	# this is the actual formula for voltage drop (one method of calculation)
	# the formula is used once for each individual circuit segment
	def final(base_current, voltage, phase, c, length, awg):
		 current = base_current * NECTables.phase_modifier(phase) * NECTables.wire_modifier(c) * length

		 numerator = current
		 denominator = NECTables.awg_to_circmils[awg]
		 
		 vd = numerator / denominator
		 percentage_1 = (voltage - vd) / voltage
		 percentage_2 = 1 - percentage_1
		 final_calc = percentage_2 * 100
		 return final_calc
