# this program takes given user inputs and uses NEC requirements to
# conclude the AWG wire size necessary to safely handle the current


from nec_tables_wd import NECTables as NEC

base_current = float(input('Load Current: '))
num_conductors = int(input('No. of Current Carrying Conductors: '))
temperature = int(input('Ambient Temperature (Fahrenheit): '))
terminals = int(input('Terminal Rating (60/75/90): '))
insulation = input('Insulation: ')
insulation = insulation.upper()
continuous = input('Continuous Load? (y/n): ')
continuous = continuous.upper()

insulation_90 = ['THHN', 'THHW', 'THW-2', 'THWN-2', 'USE-2', 'PV', 'PV WIRE', 'PV-WIRE']

insulation_75 = ['RHW', 'THHW', 'THWN', 'USE']

# NEC 310.15(B)(3)(a) adjustment factors for more than 3
# current-carrying conductors
def fill_factor(lst,num,dic):
	for i in lst:
		if num > i:
			continue
		elif num < i:
			return dic[i]
			
print('\n\n----------\n\nCORRECTION FACTORS')			
# prints fill correction factor
print('Fill Factor: %s' % fill_factor(NEC.fill_lst, num_conductors, NEC.fill_dict))


# NEC 310.15(B)(2)(a) ambient temperature correction factors
def temp_factor(lst,temp):
	if insulation in insulation_90:
		dic = NEC.temp_dict_90
	elif insulation in insulation_75:
		dic = NEC.temp_dict_75
	for i in lst:
		if temp > i:
			continue
		elif temp < i:
			return dic[i]

# prints temperature correction factor
print('Temp. Factor: %s' % temp_factor(NEC.temp_lst,temperature))

# determines the current in Amps required by the wire gauge (ampacity)
# to safely carry the load current with factored adjustments
def final_calc():
	f = fill_factor(NEC.fill_lst, num_conductors, NEC.fill_dict)
	t = temp_factor(NEC.temp_lst,temperature)
	factors = base_current / f / t
	if continuous == 'Y':
		required_ampacity = factors * 1.25
	else:
		required_ampacity = factors
	return required_ampacity
	
# prints the rounded required ampacity
print('\n----------\n\nRequired Base Ampacity: %sA\n' % round(final_calc()))

	
# these two functions determine the wire size needed based on the
# temperature rating of the terminals in the equipment being used;
# AWG then selected from NEC 310.15(B)(16) and appropriate column
def cu_wire_select(ampacity):
	if terminals == 90:
		cu_lst = NEC.cu_ampacity_90
		cu_dic = NEC.cu_ampacity_to_awg_90
	elif terminals == 75:
		cu_lst = NEC.cu_ampacity_75
		cu_dic = NEC.cu_ampacity_to_awg_75
	for a in cu_lst:
		if ampacity > a:
			continue
		elif ampacity < a:
			return cu_dic[a], a

def al_wire_select(ampacity):
	if terminals == 90:
		al_lst = NEC.al_ampacity_90
		al_dic = NEC.al_ampacity_to_awg_90
	elif terminals == 75:
		al_lst = NEC.al_ampacity_75
		al_dic = NEC.al_ampacity_to_awg_75
	for a in al_lst:
		if ampacity > a:
			continue
		elif ampacity < a:
			return al_dic[a], a
			
copper_derated = cu_wire_select(final_calc())[1] * fill_factor(NEC.fill_lst, num_conductors, NEC.fill_dict) * temp_factor(NEC.temp_lst,temperature)
aluminum_derated = al_wire_select(final_calc())[1] * fill_factor(NEC.fill_lst, num_conductors, NEC.fill_dict) * temp_factor(NEC.temp_lst,temperature)
print('----------\n\nDERATED AMPACITIES')
print('Copper Base Ampacity: %sA\nDerated Ampacity: %s\n' % (cu_wire_select(final_calc())[1],copper_derated))

print('Aluminum Base Ampacity: %sA\nDerated Ampacity: %s\n' % (al_wire_select(final_calc())[1],aluminum_derated))

# prints the appropriate wire size for both Copper and Aluminum
print('\n----------\nWIRE SIZE NEEDED:\n%s Copper\n%s Aluminum' %
(cu_wire_select(final_calc())[0], al_wire_select(final_calc())[0]))

sets = int(input('\n\n----------\n\nParallel Circuits? How many sets?: '))

dev_current = final_calc() / sets

print('\nWire size needed for %s parallel sets:\n%s Copper\n%s Aluminum' %
(sets, cu_wire_select(dev_current)[0], al_wire_select(dev_current)[0]))


