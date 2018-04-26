import federated_voting
import hashlib
import util
import message
import copy
import time

class nomination():
    def __init__(self, node_name, quorum_conf, slot_ix, slot_values, transaction_pool, ip):
        self.X = []                      # set of values node v has voted to nominate
        self.Y = []                      # set of values node v has accepted as nominated
        self.Z = []                      # set of values that node v considers candidate values
        self.N = {}                         # set of the latest NOMINATE message received from each node
        self.slot_values = slot_values
        self.slot_ix = slot_ix
        self.round = 0
        self.node_name = node_name
        self.quorum_conf = quorum_conf
        self.ip = ip
        self.transaction_pool = transaction_pool

    def handle(self, packet):
        # print(self.node_name, ' : ', packet.type, 'from ', packet.node)
        time.sleep(0.2)
        self.federated_voting(packet.data)

    def round_leader_sel(self):
        roundLeader_set = []
        neighbor_set = []
        hmax = 2**256
        topPriority = '0x00'
        threshold = self.quorum_conf['threshold']
        quorum = list(filter(lambda x : x[1][1] == 'connect', self.quorum_conf['validators'].items()))  # set of valid peers
        quorum.append((self.node_name, {'ip':0, 'status':'connect'}))
        for v in quorum:
            weight = threshold/100
            gi = self.hashFunction(v[0], 1)
            if int(weight * hmax) > eval(gi):
                neighbor_set.append(v[0])
        for v in neighbor_set:
            h = self.hashFunction(v, 2)
            if eval(h) > eval(topPriority):
                topPriority = h
                roundLeader_set = []
            if eval(h) == eval(topPriority):
                roundLeader_set.append(v)
        # print('round', self.round, ' : ', self.node_name, 'selects round leader : ', roundLeader_set)
        return roundLeader_set

    def hashFunction(self, node_name, constant_value):
        prevSlotOutput = 0 if len(self.slot_values) == 0 else self.slot_values[-1]
        hashvalue = '0x'+hashlib.sha256((str(constant_value) + str(self.round) + node_name + str(prevSlotOutput)).encode('utf-8')).hexdigest()
        return hashvalue

    def federated_voting(self, msg=None):
        r_leader_set = self.round_leader_sel()
        if msg == None:
            
            if self.node_name in r_leader_set:
                # print(self.node_name, r_leader_set)
                nominate_value = self.transaction_pool.pop(0)
                self.X.append(nominate_value)
                m = message.NominationMessage(self.node_name, self.slot_ix, self.X, self.Y, self.quorum_conf)
                self.N[self.node_name] = m
                p = util.Packet(self.node_name, self.ip, 'nomination', m)
                util.broadcast(self.quorum_conf, p)
        else:
            echoing = True if msg.node in r_leader_set else False
            self.N[msg.node] = msg
            # print(self.node_name, ' : N : ', self.N)
            self.verify_messages(echoing)
            print(self.node_name, '\'s X, Y, Z : ', self.X, self.Y, self.Z)

    def verify_messages(self, echoing=False):
        votes = {}                      # dictionary of {voted_value:count, }
        accepts = {}                    # dictionary of (accepted_value:count, }
        candidates = []                 # list of [candidates, ]
        for node in self.N.keys():
            if node != self.node_name:
                for value in self.N[node].voted_set:
                    if value not in votes.keys():
                        votes.setdefault(value, 1)
                    else:
                        votes[value] += 1	
                for value in self.N[node].accepted_set:
                    if value not in accepts.keys():
                        accepts.setdefault(value, 1)
                    else:
                        accepts[value] += 1
        if self.check_voting_count(votes, accepts, candidates, echoing):
            m = message.NominationMessage(self.node_name, self.slot_ix, self.X, self.Y, self.quorum_conf)
            p = util.Packet(self.node_name, self.ip, 'nomination', m)
            util.broadcast(self.quorum_conf, p)

    def check_voting_count(self, votes, accepts, candidates, echoing):
        if echoing:                     # flag which indicates state is changed
            state_flag = True
        else:
            state_flag = False              
        m_votes = copy.deepcopy(votes)                 # dictionary of {voted_value:count, }
        m_accepts = copy.deepcopy(accepts)             # dictionary of (accepted_value:count, }
        m_candidates = copy.deepcopy(candidates)       # list of [candidates, ]
        for value, vote_count in votes.items():
            if int(vote_count/len(self.quorum_conf['validators'])*100) >= self.quorum_conf['threshold']:
                del m_votes[value]
                state_flag = True
                if value not in m_accepts.keys():
                    m_accepts.setdefault(value, 1)
                else:
                    m_accepts[value] += 1
        for value, vote_count in accepts.items():
            if int(vote_count/len(self.quorum_conf['validators'])*100) >= self.quorum_conf['threshold']:
                del m_accepts[value]
                state_flag = True
                if value not in m_candidates:
                    m_candidates.append(value)
        for value in m_votes.keys():
            if value not in self.X:
                self.X.append(value)
        for value in m_accepts.keys():
            if value not in self.Y:
                self.Y.append(value)
        for value in m_candidates:
            if value not in self.Z:
                self.Z.append(value)
        return state_flag