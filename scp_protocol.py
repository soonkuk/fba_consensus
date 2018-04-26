import client
import fba
import message
import node
import time
import util


class ScpProtocol():
    
    def __init__(self):  # make new nodes, configure validators then node start.
        self.client = client.Client()
        self.nodes = []
        n0 = node.Node('n0', {'threshold':66, 'validators':{'n1':[5002, 'connect'], 'n2':[5003, 'connect'], 'n3':[5004, 'connect'], 'n4':[5005, 'connect']}}, 5001)  # node configure(node name, validators list, ip)
        self.nodes.append(n0)
        n1 = node.Node('n1', {'threshold':66, 'validators':{'n0':[5001, 'connect'], 'n2':[5003, 'connect'], 'n3':[5004, 'connect'], 'n4':[5005, 'connect']}}, 5002)
        self.nodes.append(n1)
        n2 = node.Node('n2', {'threshold':66, 'validators':{'n0':[5001, 'connect'], 'n1':[5002, 'connect'], 'n3':[5004, 'connect'], 'n4':[5005, 'connect']}}, 5003)
        self.nodes.append(n2)
        n3 = node.Node('n3', {'threshold':66, 'validators':{'n0':[5001, 'connect'], 'n1':[5002, 'connect'], 'n2':[5003, 'connect'], 'n4':[5005, 'connect']}}, 5004)
        self.nodes.append(n3)
        n4 = node.Node('n4', {'threshold':66, 'validators':{'n0':[5001, 'connect'], 'n1':[5002, 'connect'], 'n2':[5003, 'connect'], 'n3':[5004, 'connect']}}, 5005)
        self.nodes.append(n4)  # nodes were started
        
        
    def run(self):
        for ip in range(5001, 5006):
            for i in range(0, 5):
                self.client.send(ip, 'value'+str(i))

        for node in self.nodes:
            
            # node.ping_test()
            # node.ping_test()
            '''
            m = message.NominationMessage(node.name, 1)  # send test nomination message to all nodes
            p = util.Packet(node.name, node.ip, 'nomination', m)
            for i in range(5001, 5006):
                if node.ip == i:
                    continue
                else:
                    util.send('localhost', i, p)
            '''
            node.start_nomination()


        '''
        for node in self.nodes:     # send test 'ping' messge to '5005'
            p = util.Packet(node.name, node.ip, 'ping')
            if node.ip == 5005:
                continue
            else:
                node.send('localhost', 5005, p)
        for node in self.nodes:     # send test nomination message to all nodes
            m = util.Message(message.NominationMessage(node.name, 1))
            p = util.Packet(node.name, node.ip, 'nomination', m)
            for i in range(5001, 5006):
                if node.ip == i:
                    continue
                else:
                    node.send('localhost', i, p)
        '''

if __name__ == '__main__':
    
    protocol = ScpProtocol()
    protocol.run()
    while True:
        if input() == 'q':
            print('\n' + "// SCP protocol terminated! //" + '\n')
            break