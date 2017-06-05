"""
Shift 5 times, then xor with 5F BD 5D BD.

Idea from http://nefariousmotorsports.com/forum/index.php?topic=4983.0
"""

def start(device):
    device.open_connection()

    # Request seed
    device.send(0x32E, [0x11, 0x00, 0x02, 0x27, 0x03])

    seed1 = device.next_message().data
    seed2 = device.next_message().data
    device.send(0x32E, [0xB3])   # Ack reception of seed
    seed = seed1[5:8]
    seed.append(seed2[1])

    seed_int = int.from_bytes(seed, byteorder='big', signed=False)

    return rotate(seed_int, 5) ^ 0x5F9D7D9C

"""
Shift-Rotate <times>-times
"""
def rotate(number, times):
    if 32 -  number.bit_length()  >= times:
        # Number is small enough. No rotate needed
        return number << times
    else:
        mask = 2 ** 32 -1  # Be at most 4 Bytes long
        return ((number << times) & mask) | (number >> 32 - times)
