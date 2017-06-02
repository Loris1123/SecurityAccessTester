import reset
from device import Device


def main():
    resetalgo = reset.SerialReset('/dev/ttyACM1')
    device = Device("slcan0", resetalgo)
    device.open_connection()
    device.reset()

if __name__ == '__main__':
    main()
