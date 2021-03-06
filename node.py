import fba
import json
import socket
import pickle
import threading
import time
import util
# from signal import signal, SIGPIPE, SIG_DFL

# signal(SIGPIPE,SIG_DFL)

class Node(threading.Thread):
    def __init__(self, name, quorum_conf, ip):
        threading.Thread.__init__(self)
        self.name = name
        self.quorum_conf = quorum_conf
        self.ip = ip
        self.transactionPool = []
        self.messages = []
        self.round = round
        self.receiver = SocketReceiver(self.ip, parent=self)
        self.receiver.daemon = True
        self.receiver.start()
        self.consensus = fba.FbaConsensus(self.name, self.quorum_conf, self.transactionPool, self.ip)
        self.consensus_phase = fba.ConsensusPhase.nomination 
        self.ping = util.Packet(self.name, self.ip, 'ping')

    def ping_test(self):
        for v in self.quorum_conf['validators'].keys():
            util.send('localhost', self.quorum_conf['validators'][v][0], self.ping)

    def change_round(self):
        self.consensus.nomination.change_round()

    def packet_received(self, thread, sender_address, packet):
        if packet.type == 'ping':
            self.quorum_conf['validators'][packet.node][1] = 'connect'
            # self.ping_answer(packet.ip)
        elif packet.type == 'received_ping':
            self.quorum_conf['validators'][packet.node][1] = 'connect'
        elif packet.type == 'client_message':
            self.transactionPool.append(packet.data.message)
        else:
            self.handle_message(packet)

    def handle_message(self, packet):
        if packet.type == 'nomination' and self.consensus_phase == fba.ConsensusPhase.nomination:
            self.consensus.nomination.handle(packet)
        elif packet.type == 'prepare' and self.consensus_phase == fba.ConsensusPhase.ballot_prepare:
            self.consensus.ballot_pre.handle(packet)
        elif packet.type == 'commit' and self.consensus_phase == fba.ConsensusPhase.ballot_commit:
            self.consensus.ballot_commit.handle(packet)
        else:
            print("Message type is not compatible with consensus phase")

    def run(self):
        while True:
            self.start_nomination()

    def start_nomination(self):
        self.consensus.nomination_start()

class SocketReceiver(threading.Thread):

    def __init__(self, ip, parent=None):
        threading.Thread.__init__(self)
        self.parent = parent
        self.ip = ip

    def packet_received(self, thread, sender_address, packet):
        pass

    def run(self):
        while True:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
            self.sock.bind(('', self.ip))
            self.sock.listen(1)
            conn, addr = self.sock.accept()
            data = conn.recv(1024)
            conn.send(bytes("received", 'UTF-8'))
            self.parent and self.parent.packet_received(self, addr, pickle.loads(data))
            conn.close()
            # self.sock.close()