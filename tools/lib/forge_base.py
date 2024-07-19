class ForgeBase:
	"""Limited API for interability between diverse software forge
	(basically just opening a PR)"""
	def __init__(self):
		pass
	
	def make_pr_between_branches(self, from_branch, to_branch, title, message):
		raise NotImplementedError()
	
	def does_pr_already_exist(self, from_branch):
		raise NotImplementedError()