from device import Device

def main():
    device = Device("slcan0")
    device.open_connection()

if __name__ == '__main__':
    main()
