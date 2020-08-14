# Noctua4WireFanControl
Control Noctua Fan with MicroPython

Uses MicroPython 1.12 on an ESP32

I needed to control a 140mm Noctua fan to cool a cinema light.   The original kit made a nasty noise and had no temperature related speed control.

The key variables are duty_factor and low_pwm_limit.
duty_factor sets the response to temperature.

low_pwm_limit sets the slowest speed the fan can run at.  64 will work but the fam can be stopped by hand.  128 seems reasonable.
