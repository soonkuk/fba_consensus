import pickle
import socket
import time
import uuid
import requests
# from signal import signal, SIGPIPE, SIG_DFL
import threading
import random

# signal(SIGPIPE,SIG_DFL)

class Packet():
    def __init__(self, node, ip, message_type, message=None): 
        self.node = node                # node = sender node name
        self.ip = ip                    # ip = sender ip                 
        self.type = message_type        # message type = 'ping' or scp message type(nomination, prepare, commit, client)
        self.data = message             # message = instance of Message()


def send(host, port, packet):
    try:
        sender_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
        sender_sock.connect((host, port))
        sender_sock.sendall(pickle.dumps(packet))
        # time.sleep(2)
        # sender_sock.recv(1024)
        sender_sock.close()
    except Exception as e:
        pass

def broadcast(quorum_conf, packet):
    # receiver = list(filter(lambda x : x[1][1] == 'connect', quorum_conf['validators'].items()))
    for _, v in quorum_conf['validators'].items():
        # print(quorum_conf)
        t = threading.Thread(target = send, args=('localhost', v[0], packet, ))
        t.daemon = True
        t.start()
        time.sleep(random.randrange(1, 5))
        # print(packet.node, 'send message to', v[0], 'by broadcasting')
        #send('localhost', v[0], packet)