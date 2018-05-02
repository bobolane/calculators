class NECTables():
	
	# keys are trade size convention AWG (American Wire Gauge)
	# corresponding values are circular mils taken from NEC
	awg_to_circmils = {
	'18': 1620,
	'16': 2580,
	'14': 4110,
	'12': 6530,
	'10': 10380,
	'8': 16510,
	'6': 26240,
	'4': 41740,
	'3': 52620,
	'2': 66360,
	'1': 83690,
	'1/0': 105600,
	'2/0': 133100,
	'3/0': 167800,
	'4/0': 211600,
	'250 kcmil': 250000,
	'300 kcmil': 300000,
	'350 kcmil': 350000,
	'400 kcmil': 400000,
	'450 kcmil': 450000,
	'500 kcmil': 500000
	}

	# phase factors correspond to normal 'single phase' 3-wire systems
	# and Delta or WYE 'three-phase' 4-wire transformer configurations
	# commonly used in North America
	def phase_modifier(phase):
		if phase == 1:
			return 2
		if phase == 3:
			return (3 ** .5)

	# assumes modern uncoated Copper or Aluminum wire as described in NEC
	def wire_modifier(c):
		if c == "CU":
			return 12.9
		if c == "AL":
			return 21.2
