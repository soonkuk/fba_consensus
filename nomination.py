import federated_voting
import hashlib
import util
import message


class nomination():
    def __init__(self, node_name, quorum_conf, slot_ix, slot_values, transaction_pool, ip):
        self.X = set()
        self.Y = set()
        self.Z = set()
        self.N = {}
        self.slot_values = slot_values
        self.slot_ix = slot_ix
        self.round = 0
        self.node_name = node_name
        self.quorum_conf = quorum_conf
        self.ip = ip
        self.transaction_pool = transaction_pool

    def handle(self, packet):
        packet.data.voted_set
        #federated_voting.FederatedVoting.verify_vote_or_accepted()
        # print(packet.node, ' : ', packet.type, ' : ', packet.data.id, ' : ', packet.data.message.slot_num)
        pass

    def round_leader_sel(self):
        roundLeader_set = []
        neighbor_set = []
        hmax = 2**256
        topPriority = '0x00'
        threshold = self.quorum_conf['threshold']
        quorum = list(filter(lambda x : x[1][1] == 'connect', self.quorum_conf['validators'].items()))
        quorum.append((self.node_name, {'ip':0, 'status':'connect'}))
        # print(quorum)
        for v in quorum:
            weight = threshold/100
            gi = self.hashFunction(v[0], 1)
            if int(weight * hmax) > eval(gi):
                neighbor_set.append(v[0])
        for v in neighbor_set:
            h = self.hashFunction(v, 2)
            # print(self.node_name, ' : ', 'topPriority : ', topPriority)
            if eval(h) > eval(topPriority):
                topPriority = h
                roundLeader_set = []
            if eval(h) == eval(topPriority):
                roundLeader_set.append(v)
        # print(self.node_name, ' : ', roundLeader_set)
        return roundLeader_set

    def hashFunction(self, node_name, constant_value):
        prevSlotOutput = 0 if len(self.slot_values) == 0 else self.slot_values[-1]
        hashvalue = '0x'+hashlib.sha256((str(constant_value) + str(self.round) + node_name + str(prevSlotOutput)).encode('utf-8')).hexdigest()
        return hashvalue

    def start_federated_voting(self):
        r_leader_set = self.round_leader_sel()
        if self.node_name in r_leader_set:
            nominate_value = self.transaction_pool.pop(0)
            self.X.add(nominate_value)
            m = message.NominationMessage(self.node_name, self.slot_ix, self.X, self.Y, self.quorum_conf)
            p = util.Packet(self.node_name, self.ip, 'nomination', m)
            util.broadcast(self.quorum_conf, p)

