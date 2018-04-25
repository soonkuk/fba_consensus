import time
import uuid

class Packet():
    def __init__(self, node, ip, message_type, message=None): 
        self.node = node                # node = sender node name
        self.ip = ip                    # ip = sender ip                 
        self.type = message_type        # message type = 'ping' or scp message type(nomination, prepare, commit, client)
        self.data = message             # message = instance of Message()

class Message():
    def __init__(self, message):
        self.id = uuid.uuid1().hex
        self.message = message