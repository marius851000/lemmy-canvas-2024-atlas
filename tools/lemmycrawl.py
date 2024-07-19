import json
import os
import random
import re

#from https://www.30secondsofcode.org/python/s/slugify/
def slugify(s):
	s = s.lower().strip()
	s = re.sub(r'[^\w\s-]', '-', s)
	s = re.sub(r'[\s_-]+', '_', s)
	s = re.sub(r'^-+|-+$', '-', s)
	return s

class LemmyPostProcessor:
	def __init__(self):
		self.folder = "entries/"
		self.load_data()
	
	def load_data(self):
		self.id_to_name = {}
		for filename in os.listdir(self.folder):
			path = os.path.join(self.folder, filename)
			post = None
			with open(path, "r") as f:
				post = json.load(f)
			if post["id"] in self.id_to_name:
				raise BaseException("Duplicate ID: " + str(post["id"]))
			self.id_to_name[post["id"]] = filename

	def push_entry(self, content):
		id = None
		if content["id"] == -1:
			id = random.randint(0, 9999999999)
		else:
			id = content["id"]
		
		assert type(id) == int

		name = None
		if id in self.id_to_name:
			name = self.id_to_name[id]
		else:
			name = slugify(content["name"]) + ".json"
		
		self.id_to_name[id] = name

		with open(os.path.join(self.folder, name), "w") as f:
			json.dump(content, f, indent=4)


	def process_post(self, post_body):
		post_id = post_body["id"]
		post_body = post_body["body"]

		post_json = None
		try:
			post_json = json.loads(post_body)
		except:
			print("Post does not contain valid JSON: " + str(post_id))
			return
		
		self.push_entry(post_json)


post_processor = LemmyPostProcessor()
a = json.load(open("tools/test_post.json", "r"))["posts"][0]["post"]

post_processor.process_post(a)

"""read_ids = set()
with open("../data/lemmy_read_ids.txt", "r") as f:
	for line in f.readlines():
		if line.strip() == "":
			continue
		read_ids.add(int(line.strip()))

highest_post_id = max(read_ids) or 0

next_page = None

while True:
	req = requests.get("https://toast.ooo/api/v3/post/list", params={
		"next_page": next_page,
		"community_name": "2024lemmycanvasatlas",
		"type_": "All",
		"sort": "New",
	})
	if req.status_code != 200:
		raise BaseException("Request failed with code " + str(req.status_code))

	data = req.json()

	for post in data["posts"]:
		print(post)

		if post["i"]
	
	next_page = data["next_page"] """