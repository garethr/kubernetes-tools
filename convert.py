# Parse the CSV from the original spreadsheet listing Kubernetes configuration tools,
# and convert that to individual JSON documents

import csv
import json

from slugify import slugify

with open('seed/tools.csv', 'r') as tools:
  reader = csv.DictReader(tools)
  for row in reader:
    # slugify all the keys to make them more machine friendly
    row = {slugify(k): v for k, v in row.items()}
    # As these are all of the same type lets add a tag
    row['tags'] = ['config']
    with open("data/%s.json" % slugify(row['project']), 'w') as tool:
      json.dump(row, tool, sort_keys=True, indent=2)


