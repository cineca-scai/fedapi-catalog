# -*- coding: utf-8 -*-

"""
Example of Python code for using the API as a client
"""

# from __future__ import absolute_import

###################
import os
import json
import glob
import requests
import logging
import time

###################
PROTOCOL = 'http'
HOST = 'apiserver'
# Default is 80
PORT = os.environ.get('APISERVER_PORT', 80).split(':')[::-1][0]
URL = "%s://%s:%s/api/" % (PROTOCOL, HOST, PORT)
INPUT_DIR = '/tmp/input'

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

#######################
# Clear all data...
r = requests.get(URL + 'cleaner/all')
logger.info("Cleaned all previous data")

#######################
# Load input(s)
logger.debug("Loading from directory '%s'" % INPUT_DIR)
for filename in glob.glob(os.path.join(INPUT_DIR, "*") + ".json"):

    with open(filename, encoding='utf-8') as f:

        # Ask id: POST
        r = requests.post(main_uri, params={'owner': myuser})
        id = check_api_output(r)
        logger.info("POST: received ID %s" % id)

        # Update metadata: PUT
        try:
            data = json.load(f)
        except Exception as e:
            logger.error("Failed to read input '%s':\n%s" % (filename, e))
            exit(1)

        r = requests.put(main_uri + '/' + id, data=json.dumps(data))
        out = check_api_output(r)
        logger.info("PUT: updated: %s" % out)

logger.info("Completed data registration")
logger.warning("Debug exit. Remove this " +
               "if you'd like to test API queries in Python.")
exit(0)

# Wait for index building
time.sleep(2)

#####################################
# SUGGEST

###################
# Suggest from prefix 'my'
r = requests.get(URL + 'suggest' + '/my')
out = check_api_output(r)
logger.info("SUGGEST: %s" % out)

#####################################
# SEARCH

main_uri = URL + 'search'

###################
# Search with no parameter: GET
r = requests.get(main_uri)
out = check_api_output(r)
logger.info("SEARCH ALL: %s\n" % out)
id = out.pop()['id']

###################
# Get single results: GET
r = requests.get(URL + 'dataobjects/' + id)
out = check_api_output(r)
logger.info("SINGLE GET: %s\n" % out)

###################
# Search with parameter: POST on all fields
keyword = 'nice'
r = requests.post(main_uri, data=json.dumps({'_all': keyword}))
out = check_api_output(r)
logger.info("SEARCH filter all fields (keyword '%s'):\n%s\n" % (keyword, out))

###################
# Search with parameter: POST on specific field
field = 'format'
keyword = 'pdf'
r = requests.post(main_uri, data=json.dumps({field: keyword}))
out = check_api_output(r)
logger.info("SEARCH filter field '%s' (keyword '%s'):\n%s\n"
            % (field, keyword, out))
