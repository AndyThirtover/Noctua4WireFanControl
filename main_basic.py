# Noctua 4 wire fan control

import urequests
import network
import utime
import machine
import onewire
import ds18x20

temp_sensor_pin = machine.Pin(21)
pwm_output = machine.PWM(machine.Pin(23))
pwm_output.freq(1000)
duty = 256
duty_factor = 30
pwm_output.duty(duty)  # initial level
speed = machine.Pin(22, machine.Pin.IN)
ds = None
roms = []

#Init OneWire
def init_onewire():
	ds = ds18x20.DS18X20(onewire.OneWire(temp_sensor_pin))
	roms = ds.scan()
	for rom in roms:
		print("Found: {}".format(rom))
	return ds, roms

def read_temperature():
	try:
		ds.convert_temp()
		utime.sleep_ms(750)
		temperature = ds.read_temp(roms[0])
	except:
		temperature = 100 # return a high temperature to force a fast fan speed for safety
		init_onewire() # try to recover the onewire bus
	return temperature

ds, roms = init_onewire()

while True:
	current = read_temperature()
	duty = int(current * duty_factor)
	if duty > 1023:
		duty = 1023
	if duty < 64:
		duty = 64
	pwm_output.duty(duty)
	print("Temperature : {} Duty Cycle {} Fan Speed {}".format(current, duty, None))
	utime.sleep_ms(1000)




