# -*- coding: utf-8 -*-

"""
Example of Python code for using the API as a client
"""

# from __future__ import absolute_import

###################
import os
import json
import requests
import logging

###################
PROTOCOL = 'http'
HOST = 'apiserver'
# Default is 80
PORT = os.environ.get('APISERVER_PORT', 80).split(':')[::-1][0]
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
def check_api_output(req):
    out = req.json()
    if req.status_code > 299:
        raise BaseException("API request NOT completed:\n%s" % out)
    elif 'response' in out:
        return out['response']

    return out


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
    id = check_api_output(r)
    logger.info("POST: received ID %s" % id)

    # Update metadata: PUT
    data = json.load(f)
    r = requests.put(main_uri + '/' + id, data=json.dumps(data))
    out = check_api_output(r)
    logger.info("PUT: updated: %s" % out)

###################
# Get results: GET
r = requests.get(main_uri)
out = check_api_output(r)
logger.info("GET: %s" % out)
