import message
import pickle
import socket
import util

class Client():

    def send(self, ip, msg):
        m = message.ClientMessage(msg)
        p = util.Packet('client', None, 'client_message', m)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', ip))
        s.sendall(pickle.dumps(p))
        s.close()