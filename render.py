
import os
import glob
import json
from collections import defaultdict

import jinja2
from slugify import slugify


def render(path, context):
    path, filename = os.path.split(path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path)
    ).get_template(filename).render(context)


projects = []
tags = defaultdict(list)

OUT = 'out'

projects_dir = "%s/projects" % OUT

if not os.path.exists(OUT):
    os.makedirs(OUT)

if not os.path.exists(projects_dir):
    os.makedirs(projects_dir)

for name in glob.glob('data/*.json'):
    with open(name, 'r') as project_data:
        data = json.loads(project_data.read())

        projects.append(slugify(data['project']))

        for tag in data['tags']:
            tags[slugify(tag)].append(slugify(data['project']))

        project_page = render('templates/tool.md', data)
        with open("%s/%s.md" % (projects_dir, slugify(data['project'])), 'w') as project_out:
            project_out.write(project_page)


with open("%s/README.md" % OUT, 'w') as index_out:
    index_page = render('templates/list.md', { 'projects': projects })
    index_out.write(index_page)

for tag, projects in tags.items():
    with open("%s/%s.md" % (OUT, tag), 'w') as tag_out:
        tag_page = render('templates/list.md', { 'projects': projects })
        tag_out.write(tag_page)

