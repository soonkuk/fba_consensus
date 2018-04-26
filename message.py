import datetime
import random
import string

class ClientMessage():
    def __init__(self, message):
        self.timestamp = datetime.datetime.now()
        self.message = message

class NominationMessage():
    def __init__(self, node_name, slot_num, X={}, Y={}, D={}):
        self.timestamp = datetime.datetime.now()
        self.node = node_name
        self.slot_num = slot_num
        self.voted_set = X
        self.accepted_set = Y
        self.quorum = D

class PrepareMessage():
    def __init__(self):
        pass
    
class CommitMessage():
    def __init__(self):
        pass