"""
Adds <number> to the seed and sends it as keys
"""

def start(device, number):
    device.open_connection()

    # Request seed
    device.send(0x32E, [0x11, 0x00, 0x02, 0x27, 0x03])

    seed1 = device.next_message().data
    seed2 = device.next_message().data
    device.send(0x32E, [0xB3])   # Ack reception of seed
    seed = seed1[5:8]
    seed.append(seed2[1])

    seed_int = int.from_bytes(seed, byteorder='big', signed=False)
    # add to key
    key = seed_int + 100000

    # Parse key back.
    key = hex(key)
    key = key[2:]   # Remove "0x" from string

    byte4 = int(key[-2:],16)
    byte3 = int(key[-4:-2],16)
    byte2 = int(key[-6:-4],16)
    byte1 = int(key[-8:-6],16)

    # Send kex
    device.send(0x32E, [0x22, 0x00, 0x06, 0x27, 0x04, byte1, byte2, byte3])
    device.send(0x32E, [0x13, byte4])

    device.reset()
