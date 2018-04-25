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
    def __init__(self, name, quorumSet):
        self.node_name = name
        self.quorumSet = quorumSet
        self.slot_ix = 1
        self.slot_values = {}
        self.quorum = list(filter(lambda x : x[1] == 'connect', quorumSet['validators'].items()))
        self.nomination = nomination.nomination(self.node_name, self.quorumSet, self.slot_ix, self.slot_values)
        self.ballot_pre = ballot_prepare.ballot_prepare(self.node_name, self.quorumSet, self.slot_ix)
        self.ballot_commit = ballot_commit.ballot_commit(self.node_name, self.quorumSet, self.slot_ix)

    def isQuorumFilled(self):
        pass