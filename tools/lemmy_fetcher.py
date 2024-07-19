import json
import subprocess
from entry_manager import EntryManager
from lib.github_forge import GithubForge

class LemmyFetcher:
	def __init__(self, entry_manager):
		self.entry_manager = entry_manager
		self.forge = GithubForge()
		self.forge.from_env()
	
	
	def process_post(self, post_body, make_pr = False):
		post_id = post_body["id"]
		if self.entry_manager.is_post_processed("lemmy", post_id):
			print("Post already processed: " + str(post_id))
			return
		
		post_body = post_body["body"]

		post_json = None
		try:
			post_json = json.loads(post_body)
		except:
			print("Post does not contain valid JSON: " + str(post_id))
			return
		
		new_branch_name = "lemmy-" + str(post_id)
		if make_pr:
			if self.forge.does_pr_already_exist(new_branch_name):
				raise BaseException("PR already exists for this branch, refusing to continue: " + new_branch_name)
			# Yes, I used AI assisted tooling. And they work pretty well. Thanks codeium.
			# get git branch name
			branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
			if branch != "main":
				raise BaseException("Not on main branch, refusing to continue: " + branch)
			# check if any content in entries is dirty
			if "entries/" in subprocess.check_output(["git", "status", "--porcelain"], text=True):
				raise BaseException("Some change in entries are uncommited, refusing to continue")
			# check new branch does not already exist
			if new_branch_name in subprocess.check_output(["git", "branch", "--list", new_branch_name], text=True):
				print("Branch " + new_branch_name + " already exists, deleting it")
				subprocess.check_call(["git", "branch", "-D", new_branch_name])

			# create new branch
			subprocess.check_call(["git", "checkout", "-b", new_branch_name])

		self.entry_manager.push_entry(post_json, "lemmy", post_id)

		if make_pr:
			subprocess.check_call(["git", "add", "entries/"])
			subprocess.check_call(["git", "commit", "-m", "Add submission from Lemmy post " + str(post_id)])
			subprocess.check_call(["git", "push", "--force", "origin", new_branch_name])
			print("branch pushed, making PR")
			self.forge.make_pr_between_branches(new_branch_name, "main", "Add submission from Lemmy post " + str(post_id), "Add submission from Lemmy post " + str(post_id))
			subprocess.check_call(["git", "checkout", "main"])



	

em = EntryManager()
lm = LemmyFetcher(em)

lm.process_post(json.load(open("tools/test_post.json", "r"))["posts"][0]["post"], False)

print("done")