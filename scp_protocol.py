import client
import fba
import message
import node
import time
import util
# from signal import signal, SIGPIPE, SIG_DFL
import concurrent.futures
import random

# signal(SIGPIPE,SIG_DFL)

class ScpProtocol():
    
    def __init__(self):  # make new nodes, configure validators then node start.
        self.client = client.Client()
        self.nodes = []
        self.round = 0
        n0 = node.Node('n0', {'threshold':66, 'validators':{'n1':[5002, 'connect'], 'n2':[5003, 'connect'], 'n3':[5004, 'connect'], 'n4':[5005, 'connect']}}, 5001)  # node configure(node name, validators list, ip)
        self.nodes.append(n0)
        n1 = node.Node('n1', {'threshold':66, 'validators':{'n0':[5001, 'connect'], 'n2':[5003, 'connect'], 'n3':[5004, 'connect'], 'n4':[5005, 'connect']}}, 5002)
        self.nodes.append(n1)
        n2 = node.Node('n2', {'threshold':66, 'validators':{'n0':[5001, 'connect'], 'n1':[5002, 'connect'], 'n3':[5004, 'connect'], 'n4':[5005, 'connect']}}, 5003)
        self.nodes.append(n2)
        n3 = node.Node('n3', {'threshold':66, 'validators':{'n0':[5001, 'connect'], 'n1':[5002, 'connect'], 'n2':[5003, 'connect'], 'n4':[5005, 'connect']}}, 5004)
        self.nodes.append(n3)
        n4 = node.Node('n4', {'threshold':66, 'validators':{'n0':[5001, 'connect'], 'n1':[5002, 'connect'], 'n2':[5003, 'connect'], 'n3':[5004, 'connect']}}, 5005)
        self.nodes.append(n4)  # nodes start
        
    def run(self):
        for ip in range(5001, 5006):
            for i in range(0, 5):
                self.client.send(ip, 'value'+str(1))
        for node in self.nodes:
            node.daemon = True
            node.start()
        '''
        for i in range(50):
            time.sleep(10)
            for node in self.nodes:
                print('//////////////////////////////////////////////////')
                print(node.name, ' change round')
                print('//////////////////////////////////////////////////')
                node.consensus.nomination.change_round()
                if len(node.consensus.nomination.Z) != 0:
                    break
        ''' 

if __name__ == '__main__':
    protocol = ScpProtocol()
    protocol.run()
    while True:
        if input() == 'q':
            for node in protocol.nodes:
                print(node.consensus.nomination.X, node.consensus.nomination.Y, node.consensus.nomination.Z)
            print('\n' + "// SCP protocol terminated! //" + '\n')
            break