# -*- coding: utf-8 -*-

"""
Example of Python code for using the API as a client
"""

# from __future__ import absolute_import

###################
import json
import requests
import logging

###################
PROTOCOL = 'http'
HOST = 'apiserver'
# PORT = 5000
PORT = 80
URL = "%s://%s:%s/api/" % (PROTOCOL, HOST, PORT)

###################
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

###################
headers = {
    'content-type': 'application/json',
    # 'Authentication-Token': g.user.token
}
# opts = {'stream': True, 'headers': headers, 'timeout': 5}

main_uri = URL + 'dataobjects'
myuser = 'pdonorio'

###################
with open("input.json", encoding='utf-8') as f:

    # Ask id: POST
    r = requests.post(main_uri, params={'owner': myuser})
    id = r.json()
    logger.info("POST: received id '%s'" % id)

    # Update metadata: PUT
    data = json.load(f)
    r = requests.put(main_uri + '/' + id, data=json.dumps(data))
    logger.info("PUT: updated. Out = %s" % r.json())

###################
# Get results: GET
r = requests.get(main_uri)
logger.info("GET: %s" % r.json())
