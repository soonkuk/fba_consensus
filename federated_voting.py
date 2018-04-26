class FederatedVoting():
	def __init__(self, quorum_set):
		self.threshold = quorum_set['threshold']
		self.quorum = quorum_set['validators']

	def verify_vote_or_accepted(self): 	# verify reached agreement by quorum threshold 
		pass

	def verify_accepted(self):			# verify reached agreement by quorum threshold
		pass
	
	def verify_confirm(self):
		pass
