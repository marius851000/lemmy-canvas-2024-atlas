import json
import subprocess
import requests
import os
import traceback
from entry_manager import EntryManager
from lib.github_forge import GithubForge

class LemmyFetcher:
	def __init__(self, entry_manager):
		self.entry_manager = entry_manager
		self.forge = GithubForge()
		self.forge.from_env()
		self.read_ids = set()
		os.makedirs("processed_posts", exist_ok = True)
		for filename in os.listdir("processed_posts"):
			self.read_ids.add(filename)
		
		login_req = requests.post("https://toast.ooo/api/v3/user/login", json={
			"username_or_email": os.environ.get("LEMMY_USERNAME"),
			"password": os.environ.get("LEMMY_PASSWORD"),
			"totp_2fa_token": "",
		})
		print(login_req.content)
		assert login_req.status_code == 200
		self.lemmy_jwt = login_req.json()["jwt"]
	
	
	def process_post(self, post_body, make_pr = False):
		post_id = post_body["id"]

		if str(post_id) in self.read_ids:
			print("Post already processed: " + str(post_id))
			return
		
		if self.entry_manager.is_post_processed("lemmy", post_id):
			print("Post already used in an entry: " + str(post_id))
			return
		
		if "body" not in post_body:
			print("Post does not contain body: " + str(post_id))
			return
		
		post_body = post_body["body"]

		post_json = None
		try:
			post_json = json.loads(post_body)
		except:
			print("Post does not contain valid JSON: " + str(post_id))
			self.send_comment(post_id, "An error occurred while parsing this post. Maybe it’s just not a submission, but if it should, then it is not well formatted.")
			return
		
		new_branch_name = "lemmy-" + str(post_id)
		if make_pr:
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

		success = True
		try:
			self.entry_manager.push_entry(post_json, "lemmy", post_id)
		except Exception as e:
			print("Failed to process post " + str(post_id) + ": " + str(e))
			success = False

		if make_pr:
			if success:
				subprocess.check_call(["git", "add", "entries/"])
				subprocess.check_call(["git", "commit", "-m", "Add submission from Lemmy post " + str(post_id)])
				subprocess.check_call(["git", "push", "--force", "origin", new_branch_name])
				pr_url = self.forge.does_pr_already_exist(new_branch_name)
				if pr_url == False:
					print("branch pushed, making PR")
					pr_url = self.forge.make_pr_between_branches(new_branch_name, "main", "Add submission from Lemmy post " + str(post_id), "An automated PR for submission " + str(post_id))
				else:
					print("branch pushed, PR already exists")
				self.send_comment(post_id, "Thanks for your submission! The automatic PR has been opened at: " + pr_url)
			else:
				subprocess.check_call(["git", "restore", "--source=HEAD", "entries/"])
			subprocess.check_call(["git", "checkout", "main"])
			self.read_ids.add(str(post_id))
			f = open("processed_posts/" + str(post_id), "w")
			f.close()
	
	def send_comment(self, post_id, comment):
		req = requests.post("https://toast.ooo/api/v3/comment", json={
			"content": comment,
			"post_id": post_id,
		}, headers = {
			"Authorization": "Bearer " + self.lemmy_jwt
		})
		print(req.content)
		assert req.status_code == 200
		print("Commented on post " + str(post_id))

	def crawl_latest(self):
		req = requests.get("https://toast.ooo/api/v3/post/list", params={
			"community_name": "2024lemmycanvasatlas",
			"type_": "All",
			"sort": "New",
			"limit": 50
		})
		if req.status_code != 200:
			raise BaseException("Request failed with code " + str(req.status_code))
		
		data = req.json()

		for post in data["posts"]:
			try:
				self.process_post(post["post"], True)
			except Exception as e:
				print("Failed to process post in an horrible way: " + str(post["post"]["id"]) + ": " + str(e))
				print(traceback.format_exc())
				subprocess.check_call(["git", "checkout", "main"])


em = EntryManager()
lm = LemmyFetcher(em)
lm.crawl_latest()