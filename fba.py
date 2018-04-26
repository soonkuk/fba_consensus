import nomination
import ballot_prepare
import ballot_commit
import enum

class ConsensusPhase(enum.Enum):
    nomination = enum.auto()
    ballot_prepare = enum.auto()
    ballot_commit = enum.auto()
    externalize = enum.auto()

class FbaConsensus():
    def __init__(self, name, quorum_conf, transaction_pool, ip):
        self.node_name = name
        self.quorum_conf = quorum_conf
        self.ip = ip
        self.slot_ix = 1
        self.slot_values = {}
        self.transaction_pool = transaction_pool
        self.quorum = list(filter(lambda x : x[1][1] == 'connect', self.quorum_conf['validators'].items()))
        self.nomination = nomination.nomination(self.node_name, self.quorum_conf, self.slot_ix, self.slot_values, self.transaction_pool, self.ip)
        self.ballot_pre = ballot_prepare.ballot_prepare(self.node_name, self.quorum_conf, self.slot_ix)
        self.ballot_commit = ballot_commit.ballot_commit(self.node_name, self.quorum_conf, self.slot_ix)
        self.consensu_phase = ConsensusPhase.nomination

    def isQuorumFilled(self):
        pass

    def nomination_start(self):
        self.nomination.federated_voting()