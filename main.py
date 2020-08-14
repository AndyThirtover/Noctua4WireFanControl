# Noctua 4 wire fan control
# We only expect to find one temperature sensor

import urequests
import network
import utime
import machine
import onewire
import ds18x20
from machine import Pin, time_pulse_us, disable_irq, enable_irq

temp_sensor_pin = machine.Pin(21)
pwm_output = machine.PWM(machine.Pin(23))
pwm_output.freq(1000)
duty = 256
duty_factor = 25
low_pwm_limit = 128    # lowest speed we allow the fan to go
pwm_output.duty(duty)  # initial level
speed = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_UP)
ds = None
roms = []
tau = 0.25  # averaging factor
res = 0     # running average inverse (how many pulses before a state change)

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

def median_of_n(p, n, timeout):
    set = []
    for _ in range(n):
        time_pulse_us(p, 1, timeout)
        v = time_pulse_us(p, 1, timeout)
        time_pulse_us(p, 0, timeout)
        v += time_pulse_us(p, 0, timeout)
        set.append(v)
    set.sort()
    return set[n//2]

ds, roms = init_onewire()

while True:
	current = read_temperature()
	duty = int(current * duty_factor)
	if duty > 1023:
		duty = 1023
	if duty < low_pwm_limit:
		duty = low_pwm_limit
	pwm_output.duty(duty)
	# get an approximate fan speed and average it
	res += tau * (median_of_n(speed, 2, 55000) - res)
	print("Temperature : {} Duty Cycle {} Fan Speed {}".format(current, duty, 1000000/res))
	utime.sleep_ms(1000)




