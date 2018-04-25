import message
import node
import fba
import util
import time

class ScpProtocol():
    
    def __init__(self):  # make new nodes, configure validators then node start.
        self.nodes = []
        n0 = node.Node('n0', ['n1', 'n2', 'n3', 'n4'], 5001)  # node configure(node name, validators list, ip)
        self.nodes.append(n0)
        n1 = node.Node('n1', ['n0', 'n2', 'n3', 'n4'], 5002)
        self.nodes.append(n1)
        n2 = node.Node('n2', ['n0', 'n1', 'n3', 'n4'], 5003)
        self.nodes.append(n2)
        n3 = node.Node('n3', ['n0', 'n1', 'n2', 'n4'], 5004)
        self.nodes.append(n3)
        n4 = node.Node('n4', ['n0', 'n1', 'n2', 'n3'], 5005)
        self.nodes.append(n4)  # nodes were started
        
    def run(self):
        for node in self.nodes:     # send test 'ping' messge to all nodes
            p = util.Packet(node.name, node.ip, 'ping')
            for i in range(5001, 5006):
                if node.ip == i:
                    continue
                else:
                    node.send('localhost', i, p)
        for node in self.nodes:     # send test nomination message to all nodes
            m = util.Message(message.NominationMessage(node.name, 1))
            p = util.Packet(node.name, node.ip, 'nomination', m)
            for i in range(5001, 5006):
                if node.ip == i:
                    continue
                else:
                    node.send('localhost', i, p)

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