from github import Auth
from github import Github

from lib.forge_base import ForgeBase
import os

class GithubForge(ForgeBase):
	def __init__(self):
		self.github = None
		self.repo = None
		pass
	
	def from_env(self):
		self.github_token = os.environ.get("GITHUB_TOKEN")
		self.owner_name = os.environ.get("GITHUB_OWNER")
		self.repo_name = os.environ.get("GITHUB_REPO_NAME")

	def load(self):
		auth = Auth.Token(self.github_token)
		self.github = Github(auth = auth)
		self.repo = self.github.get_repo(self.owner_name + "/" + self.repo_name)
	
	def load_if_needed(self):
		if self.github is None:
			self.load()
	
	def does_pr_already_exist(self, from_branch):
		self.load_if_needed()

		print("check PR for " + self.owner_name + ":" + from_branch)
		for pr in self.repo.get_pulls(state="open", head=self.owner_name + ":" + from_branch):
			return pr.html_url

		return False
	
	def make_pr_between_branches(self, from_branch, to_branch, title, body):
		self.load_if_needed()

		return self.repo.create_pull(
			title = title,
			base = to_branch,
			head = from_branch,
			body = body
		).html_url