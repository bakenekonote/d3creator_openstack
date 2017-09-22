#!/usr/bin/env python
import ipaddress
import json
from jinja2 import Environment, FileSystemLoader
from argparse import ArgumentParser
import os.path

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file handle
        
#string has to be in unicode!
loopback_SUPERNET=u'192.168.255.0/24'
LINKS_SUPERNET=u'192.168.0.0/16'

# prefix must be a integer!
LINKS_SUBNET_PREFIX=24

links_subnets = list(ipaddress.ip_network(LINKS_SUPERNET).subnets(new_prefix=LINKS_SUBNET_PREFIX))

parser = ArgumentParser(description="D3 Creater HEAT Config Generator")
parser.add_argument("-i", dest="filename", required=True,
                    help="input json file", metavar="FILE",
                    type=lambda x: is_valid_file(parser, x))
args = parser.parse_args()

data = json.load(args.filename)

mxs = [ x for x in data['nodes'] if x['type'] == "mx"]
ubuntus = [ x for x in data['nodes'] if x['type'] == "ubuntu"]
links = data['links']

for link in links:
  link['subnet'] = str(links_subnets.pop(0))

for mx in mxs:
  mx['links'] = []
  for link in links:
    if link['source']['name'] == mx['name'] or link['target']['name'] == mx['name']:
      mx['links'].append(link)

for ubuntu in ubuntus:
  ubuntu['links'] = []
  for link in links:
    if link['source']['name'] == ubuntu['name'] or link['target']['name'] == ubuntu['name']:
      ubuntu['links'].append(link)

j2_env = Environment(loader=FileSystemLoader('.'), trim_blocks=True)
print j2_env.get_template('openstack_heat_template_networks.j2').render(mxs=mxs, links=data['links'], ubuntus=ubuntus)
