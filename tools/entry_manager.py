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

class EntryManager:
	def __init__(self):
		self.folder = "entries/"
		self.load_data()
	
	def load_data(self):
		self.id_to_name = {}
		self.combined_source_list = {}
		for filename in os.listdir(self.folder):
			path = os.path.join(self.folder, filename)
			entry = None
			with open(path, "r") as f:
				entry = json.load(f)
			if entry["id"] in self.id_to_name:
				raise BaseException("Duplicate ID: " + str(entry["id"]))
			self.id_to_name[entry["id"]] = filename
			if "source_list" in entry:
				for (source_name, source_list) in entry["source_list"].items():
					if source_name in self.combined_source_list:
						self.combined_source_list[source_name].extend(source_list)
					else:
						self.combined_source_list[source_name] = source_list

	def push_entry(self, content, source_name = None, source_id = None):
		id = None
		if content["id"] == -1:
			id = None
			while id is None or id in self.id_to_name:
				id = random.randint(0, 9999999999)
			content["id"] = id
		else:
			id = content["id"]
		
		assert type(id) == int

		name = None
		if id in self.id_to_name:
			name = self.id_to_name[id]
		else:
			name = slugify(content["name"]) + ".json"
		
		self.id_to_name[id] = name

		if source_name is not None and source_id is not None:
			if "source_list" not in content:
				content["source_list"] = {}

			if source_name in content["source_list"]:
				content["source_list"][source_name].append(source_id)
			else:
				content["source_list"][source_name] = [source_id]
			
			if source_name in self.combined_source_list:
				self.combined_source_list[source_name].append(source_id)
			else:
				self.combined_source_list[source_name] = [source_id]

		with open(os.path.join(self.folder, name), "w") as f:
			json.dump(content, f, indent=4)
	
	def entry_by_id_if_exist(self, id):
		return self.id_to_name.get(id)
	
	def is_post_processed(self, source_name, source_id):
		if source_name in self.combined_source_list:
			return source_id in self.combined_source_list[source_name]
		return False

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