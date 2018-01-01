#!/usr/bin/python
import max31855
import time
m = max31855.Max31855()

while True:
	m.take_reading()
	print("Fault? %s Therm: %f Chip: %f Fault: %s"%(str(m.is_faulted()), m.thermocouple_temp_f(), m.internal_temp_f(), m.fault_reason()))
	time.sleep(0.1)
