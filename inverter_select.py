

module_size = int(input("Module size in Watts: "))
module_qnty = int(input("Number of modules: "))
#module_volts = int(input("Module Voc: "))
inverter = input("Inverter brand: ")
inverter = inverter.upper()

system_size = ((module_size * module_qnty) / 1000)

print("System size: %skW" % system_size)

sub_arrays = int(input("Number of sub arrays: "))

arrays_azimuths = {}
array_modules = {}

for array in range(sub_arrays):
	array = array +1
	azimuth = int(input("Azimuth for array %s: " % array))
	array_size = int(input("Modules quantity for array %s: " % array))
	array_modules[array] = array_size
	arrays_azimuths[array] = azimuth
	
print(arrays_azimuths)
print(array_modules)

if all(value == 180 for value in arrays_azimuths.values()) is True:
	derate = .9
else:
	derate = .85
	
print(derate)

inverter_capacity = (system_size * 1000) * derate
print(inverter_capacity)



sma_dict = {
	3.1: "SB 3.0-US",
	3.9: "SB 3.8-US",
	5.1: "SB 5.0-US",
	6.1: "SB 6.0-US",
	7.1: "SB 7.0-US",
	7.8: "SB 7.7-US"
	}
	
sma_lst = [3.1, 3.9, 5.1, 6.1, 7.1, 7.8]



def inverter_qnty():
	if inverter == "SMA":
		if 1 <= (system_size / 9) < 2:
			return 2
		elif 2 <= (system_size / 9) < 3:
			return 3
		else:
			return 1

print(inverter_qnty())

def inverter_sizes(lst, dct):
	if inverter_qnty() == 1:
		for i in lst:
			if (system_size * derate) > i:
				continue
			elif (system_size * derate) <= i:
				return dct[i]
	if inverter_qnty() == 2:
		inverter_one = sma_dict[7.8]
		for i in lst:
			remainder = system_size - 7.8
			if remainder > i:
				continue
			elif remainder <= i:
				inverter_two = sma_dict[i]
				return inverter_one, inverter_two

print(inverter_sizes(sma_lst, sma_dict))


