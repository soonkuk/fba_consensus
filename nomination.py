import hashlib

class nomination():
    def __init__(self, node_name, quorumSet, slot_ix, slot_values):
        self.X = {}
        self.Y = {}
        self.Z = {}
        self.N = {}
        self.slot_values = slot_values
        self.slot_ix = slot_ix
        self.round = 0
        self.node_name = node_name
        self.qset = quorumSet

    def handle(self, packet):
        self.round_leader_sel()
        # print(packet.node, ' : ', packet.type, ' : ', packet.data.id, ' : ', packet.data.message.slot_num)
        pass

    def round_leader_sel(self):
        roundLeader_set = []
        neighbor_set = []
        hmax = 2**256
        topPriority = '0x00'
        threshold = self.qset['threshold']
        quorum = list(filter(lambda x : x[1] == 'connect', self.qset['validators'].items()))
        quorum.append((self.node_name, 'connect'))
        print(quorum)
        for v in quorum:
            weight = threshold/100
            gi = self.hashFunction(v[0], 1)
            if int(weight * hmax) > eval(gi):
                neighbor_set.append(v)
        for v in neighbor_set:
            h = self.hashFunction(v[0], 2)
            print(self.node_name, ' : ', 'topPriority : ', topPriority)
            if eval(h) > eval(topPriority):
                topPriority = h
                roundLeader_set = []
            if eval(h) == eval(topPriority):
                roundLeader_set.append(v)
        print(self.node_name, ' : ', roundLeader_set)
        return roundLeader_set

    def hashFunction(self, node_name, constant_value):
        prevSlotOutput = 0 if len(self.slot_values) == 0 else self.slot_values[-1]
        hashvalue = '0x'+hashlib.sha256((str(constant_value) + str(self.round) + node_name + str(prevSlotOutput)).encode('utf-8')).hexdigest()
        return hashvalue

    def nominationFederate(self):
        pass