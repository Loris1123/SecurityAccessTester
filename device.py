import can
from threading import Thread
from time import sleep

"""
Class for maintaining the connection to the CAN device.

Note: This is a dumb class. It will only send and receive messages. Everything else (Like ACKing packages) needs to be done by the components using this class.
"""
class Device(object):

    def __init__(self, bus, reset):
        self.bus = can.interface.Bus(channel=bus, bustype='socketcan_native')
        self.buffered_messages = []
        self.reading = True

        # Start read thread
        self.thread = Thread(target=self.read)
        self.thread.start()
        self.resetalgo = reset

    """
    Opens a channel and starts a diagnostic session.
    TODO: Dynamic sender-receiver ID
    """
    def open_connection(self):
        self.send(0x200, [0x1F, 0xC0, 0x00, 0x10, 0x00, 0x03, 0x01])
        self.next_message()
        self.send(0x32E, [0xA0, 0x0F, 0x8A, 0xFF, 0x32, 0xFF])
        self.next_message()
        self.send(0x32E, [0x10, 0x00, 0x02, 0x10, 0x89])
        self.next_message()
        self.send(0x32E, [0xB1])


    """
    Send a message to CANbus
    """
    def send(self, id, data):
        msg = can.Message(arbitration_id=id, data=data,  extended_id=False)
        self.bus.send(msg)
        sleep(0.02)   # 20ms. Wait for a possile response

    """
    Returns the next message from the buffer and removes it
    """
    def next_message(self):
        while len(self.buffered_messages) == 0:   # REMOVE!!!!
            sleep(0.02)
        return self.buffered_messages.pop()

    def read(self):
        while self.reading:
            msg = self.bus.recv()
            if len(msg.data) > 1:
                self.buffered_messages.insert(0, msg)
                # Else ACK(B*) or A*

    """
    Invokes the reset algorithm specified in constructor
    """
    def reset(self):
        self.resetalgo.reset()
