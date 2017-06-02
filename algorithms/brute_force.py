"""
Simple brute forcer.
Trying random keys without evaluating the received seed.
"""

def start(device):
    print("Go")
    device.open_connection()
    device.reset()
