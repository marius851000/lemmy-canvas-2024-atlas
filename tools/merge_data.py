import json
import sys
import os


def usage():
	print("Usage: python merge_data.py SOURCE_DIR TARGET_FILE")
	print("Merge data from multiple JSON files in SOURCE_DIR into TARGET_FILE")

if len(sys.argv) != 3:
	usage()
	sys.exit(1)

SOURCE_DIR = sys.argv[1]
TARGET_FILE = sys.argv[2]

result = []
for filename in os.listdir(SOURCE_DIR):
	path = os.path.join(SOURCE_DIR, filename)
	with open(path, "r") as f:
		result.append(json.load(f))

with open(TARGET_FILE, "w") as f:
	json.dump(result, f)

print("Done")