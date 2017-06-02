"""
Contains different reset algorithms
"""

"""
When no reset is required
"""
class NoReset():
    def reset(self):
        pass
"""
A device is connected via a serial port to pull the PORST Port of the
microcontroller to low.
"""
import serial
class SerialReset():
    def __init__(self, serialport, baudrate=9600):
        self.ser = serial.Serial(serialport, baudrate, timeout=1)

    def reset(self):
        self.ser.write(1)
