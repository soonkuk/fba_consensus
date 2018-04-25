import fba
import json
import socket
import pickle
import threading

class Node():

    def __init__(self, name, validators, ip):
        threading.Thread.__init__(self)
        self.name = name
        self.quorumSet = {}
        self.quorumSet.setdefault('threshold', 66)
        self.quorumSet.setdefault('validators', {})
        self.ip = ip
        self.transactionPool = []
        self.messages = []
        self.receiver = SocketReceiver(self.ip, parent=self)
        self.receiver.daemon = True
        self.receiver.start()
        for v in validators:
            self.quorumSet['validators'][v] = 'no conn'
        self.consensus = fba.FbaConsensus(self.name, self.quorumSet)
        self.consensus_phase = fba.ConsensusPhase.nomination

    def send(self, host, port, packet):
        sender_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
        sender_sock.connect((host, port))
        sender_sock.send(pickle.dumps(packet))

    def packet_received(self, thread, sender_address, packet):
        if packet.type == 'ping':
            self.quorumSet['validators'][packet.node] = 'connect'
            # print('sender - ', packet.node, ' : ', self.name, '\'s validators network state : ', self.quorumSet['validators'])
        elif packet.type == 'client':
            self.transactionPool.append(packet)
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

class SocketReceiver(threading.Thread):

    def __init__(self, ip, parent=None):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
        self.sock.bind(('', ip))
        self.parent = parent

    def packet_received(self, thread, sender_address, packet):
        pass

    def run(self):
        while True:
            self.sock.listen(1)
            self.conn, self.addr = self.sock.accept()
            data = self.conn.recv(1024)
            self.parent and self.parent.packet_received(self, self.addr, pickle.loads(data))