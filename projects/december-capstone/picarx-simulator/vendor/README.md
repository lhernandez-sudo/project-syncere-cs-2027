# SunFounder PiCar-X source

Source is from https://github.com/sunfounder/picar-x at revision
897698daf2719d830a5fb0b83951704bfee07d0c, from the 2.1.x branch.
The license is included as LICENSE.picar-x.

The only change to sunfounder_picarx.py is a guarded robot_hat import that allows
desktop simulation subclasses to load without Raspberry Pi libraries.
The physical constructor fails explicitly when robot_hat is unavailable.
The upstream motor, steering, calibration, and sensor methods are retained.
