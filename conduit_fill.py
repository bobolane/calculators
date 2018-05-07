# this program takes user inputs to find total conductor cross-sectional
# area and selects the appropriate conduit trade size to keep the
# conduit fill below 40%.

from nec_tables_cf import NECTables


conductor_gauge = input("AWG#: ")
conductor_type = input("Insulation type: ")
num_conductors = int(input("No. of Conductors: "))
ground = input("Equipment Ground Size: ")
conduit_type = input("Conduit Type: ")

thhn_alt_names = ['thhn', 'thwn', 'thwn-2']
rhh_alt_names = ['rhh', 'rhw', 'rhw-2', 'pv', 'pv wire', 'pv-wire']

# this function retrieves the cross-sectional area for the
# wire gauge given by the user
def conductor_value(alt_name, gauge, dic):
  if conductor_type in alt_name:
    for key in dic:
      if gauge == key:
        return dic[key]

print(conductor_value(rhh_alt_names, conductor_gauge, NECTables.rhh_awg_to_area))

thhn = conductor_value(thhn_alt_names, conductor_gauge, NECTables.thhn_awg_to_area)
rhh = conductor_value(rhh_alt_names, conductor_gauge, NECTables.rhh_awg_to_area)

# calculates the total cross-sectional area based on no. of conductors
if conductor_type in rhh_alt_names:
  area = rhh * num_conductors + NECTables.rhh_awg_to_area[ground]
elif conductor_type in thhn_alt_names:
  area = (thhn * num_conductors) + NECTables.thhn_awg_to_area[ground]

# based on total wire cross-sect area, this function retrieves
# the smallest trade size conduit where conduit fill is no larger
# than 40%
def conduit_select(y,z):
	for x in y:	
		if (area / .4) > x:
			continue
		elif (area / .4) < x:
			cross_sect = (area / x) * 100
			return cross_sect, z[x]
			
# prints the conduit fill and trade size
if conduit_type == 'emt':
	final = conduit_select(NECTables.emt_lst,NECTables.emt_dict)
	print('\n\n--------\n\nConduit fill:\n%.3f%% in %s EMT.' %
	(final[0],final[1]))
elif conduit_type == 'pvc':
	final = conduit_select(NECTables.pvc_lst,NECTables.pvc_dict)
	print('\n\n--------\n\nConduit fill:\n%.3f%% in %s PVC.' %
	(final[0],final[1]))
	
# allows user to manually select conduit trade size and calculates
# fill percentage based on variable inputs from earlier
print('\n--------\n\nFor manual conduit sizing using above conductor variables, press')
enter = input('ENTER: ')

conduit_type_manual = input('Conduit Type: ')
conduit_size_manual = input('Conduit Trade Size: ')

if conduit_type_manual == 'emt':
	conduit_type_manual = conduit_type_manual.upper()
	for key, value in NECTables.emt_dict.items():
		if value == conduit_size_manual:
			manual = (area / key) * 100
			
if conduit_type_manual == 'pvc':
	conduit_type_manual = conduit_type_manual.upper()
	for key, value in NECTables.pvc_dict.items():
		if value == conduit_size_manual:
			manual = (area / key) * 100

print('\n--------\n\nConduit fill:\n%.2f%% in %s %s.' %
(manual, conduit_size_manual, conduit_type_manual))

	
