# -*- coding: utf-8 -*-

"""
Example of Python code for using the API as a client
"""

# from __future__ import absolute_import

import requests
import json

PROTOCOL = 'http'
HOST = 'apiserver'
PORT = 5000
URL = "%s://%s:%s/api/" % (PROTOCOL, HOST, PORT)

headers = {
    'content-type': 'application/json',
    # 'Authentication-Token': g.user.token
}
# opts = {'stream': True, 'headers': headers, 'timeout': 5}

main_uri = URL + 'dataobjects'

with open("input.json", encoding='utf-8') as f:
    # Write
    data = json.load(f)
    r = requests.post(main_uri, data=json.dumps(data))
    out = r.json()
    print("TEST", out)

# # Read
# r = requests.get(main_uri)
# out = r.json()
# print("TEST", out)
