import reset
from device import Device

from algorithms import brute_force
from algorithms import adder
from algorithms import shiftxor

def main():
    resetalgo = reset.SerialReset('/dev/ttyACM1')
    device = Device("slcan0", resetalgo)

    # Device and reset algorithm had been configured.
    # No try algorithms

    #brute_force.start(device)
    #adder.start(device, 70000)
    shiftxor.start(device)

if __name__ == '__main__':
    main()
