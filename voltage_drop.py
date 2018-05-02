# this voltage drop calculator is intended for
# residential/commercial/industrial building wiring as governed
# in the NFPA 70 National Electrical Code (NEC)
# this method uses constant values for conductor material and does not
# take into account resistance in ohms/ft tables provided in NEC


from nec_tables_vd import NECTables
from final_calc_vd import FinalCalc

# for multi-series circuits
segments = int(input('How many circuit segments?: '))
print('')

# these values will not change, regardless of number of segments
base_current = float(input('Current: '))
voltage = int(input('Voltage: '))
phase = int(input('Phase 1 or 3: '))
print('\n--------\n')

# this list used to compile segment values if segments > 1
vd_values = []

# input variables pertaining to individual circuit segments
for segment in range(segments):
	segment_number = segment + 1
	print('***Segment %s***' % segment_number)
	wire_type = input('cu or al: ')
	c = wire_type.upper()
	length = int(input('Circuit Length (ft.): '))
	while True:
		awg = input('AWG#: ')
		if awg in NECTables.awg_to_circmils:
			break
		else:
			print('Sorry, enter values such as "10", "6", "3/0", or "250 kcmil"')
			continue
			
	
	segment_total = FinalCalc.final(base_current, voltage, phase, c, length, awg)
	if segments == 1:
		vd_values.append(segment_total)
		break
	else:
		print('VD for segment %s: %.3f%%\n' % (segment_number, segment_total))
		vd_values.append(segment_total)


print('\n--------\n\n***Total***\nTotal voltage drop is %.3f%%.' % sum(vd_values))
