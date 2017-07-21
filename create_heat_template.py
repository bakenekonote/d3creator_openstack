#!/usr/bin/env python

import json
from jinja2 import Environment, FileSystemLoader

with open('input.json') as data_file:
    data = json.load(data_file)

mxs = [ x for x in data['nodes'] if x['type'] == "mx"]
ubuntus = [ x for x in data['nodes'] if x['type'] == "ubuntu"]
links = data['links']

for mx in mxs:
  mx['links'] = []
  for link in links:
    if link['source']['name'] == mx['name'] or link['target']['name'] == mx['name']:
      mx['links'].append(link)

j2_env = Environment(loader=FileSystemLoader('.'), trim_blocks=True)
print j2_env.get_template('openstack_heat_template.j2').render(mxs=mxs, p2plinks=data['links'])

