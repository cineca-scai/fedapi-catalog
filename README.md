
## API catalog *prototype*

This project is intented to test the behavior of a REST API server which fills one or more cache database (`neo4j`, `elasticsearch`, etc.) for a catalog service.


### Data model

* The neomodels mapping of our data into a graph db can be found [here](vanilla/models/neo4j.py).
* The DSL models for elasticsearch indexes can be found [inside this file](vanilla/models/elasticsearch.py)
* The implementation of current endpoints is available at [this python class](vanilla/apis/fedapp.py)


### Pre-requisites

Before starting please make sure that you have installed on your system:

* [docker](http://docs.docker.com/) 1.11+
* [docker-compose](https://docs.docker.com/compose/) 1.7+


### Run the main server

Clone the repository.
Then, from a terminal at the very root of the repo:

```bash

# Run the docker stack
$ ./do DEVELOPMENT

[...]
Docker stack: booting
[...]
Stack processes:
[...]
```

### Implemented endpoints

#### dataobjects

* GET `/api/dataobjects/:ID`
finds the objects stored inside the graphdb

* POST `/api/dataobjects` {user: 'myuser'}
creates a new dataobjects beloing to 'myuser', replying with a new registered ID

* PUT `/api/dataobjects/ID` {user: 'myuser', ... JSON DATA ...}
updates the dataobject to save the JSON DATA inside the graphdb and elasticsearch

#### suggestion

* GET `/api/suggest/PREFIX`
looks for any term of the current catalog fitting the provided PREFIX

#### search and filter

* GET `/api/search`
get all data from elasticsearch

* POST `/api/search` {_all: 'term'}
search for 'term' in any field of the elasticsearch objects

* POST `/api/search` {key1: 'value1', ..., keyN: 'valueN'}
filter with all 'value' in specified `key` field of all elasticsearch objects

### Query the REST API server

We may query the server from a client container

```bash
# Open a client container
$ ./do client_shell

# Check if the server is reachable

/code $ http apiserver/api/status
{
  "response": "Server is alive!"
}
```


### Insert some data

The client container has a script to populate the catalog
with all the `JSON` files found inside [the vanilla directory](vanilla/input):

```bash

# Run the python client to create data inside the GraphDB
/code $ python3 register.py
2016-07-07 08:09:05,608 __main__     INFO     POST: received id 'aa90135e-7242-4790-a389-1500b67074a9'
2016-07-07 08:09:06,506 __main__     INFO     PUT: updated. Out = aa90135e-7242-4790-a389-1500b67074a9
2016-07-07 08:09:06,525 __main__     INFO     GET: Hello world
```


### Query the REST API server

You may query directly the API with `curl` from your host command line:
```bash
curl -i http://localhost:8080/api/status
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 37
Server: Werkzeug/0.11.10 Python/3.5.1+
Date: Tue, 26 Jul 2016 16:00:28 GMT

{
  "response": "Server is alive!"
}
```

Usually we test our APIs with the great [`httpie` tool](http://httpie.org),
which you find already installed inside the client container:
```bash

/code # http apiserver/api/dataobjects
HTTP/1.0 200 OK

{
    "response": [
        {
            "attributes": {
                "logicalName": ...
            },
            "id": "db7a16e2-4222-4d23-a8c7-75bfaa445bd3",
            "links": {
            },
            "relationships": {
            }
[...]
}

```

Interesting queries to test:

* Ask for suggestions on a certain prefix across all terms:
```
http apiserver/api/suggest/ha
```

* Get a single element:
```
# SYNTAX: http apiserver/api/dataobjects/<ID>, e.g.:
http apiserver/api/dataobjects/c119e4e0-07cc-455d-88a1-7d78ac5c777a
```

* Search a term in all textual fields:
```
http POST apiserver/api/search _all=42
```

* Search a term in a specific field:
```
http POST apiserver:5000/api/search tags=nice
http POST apiserver:5000/api/search format=pdf
```

Note: suggestion + search (both based on `elasticsearch`) are the usual component used as backend for a Javascript web page that implements a Google-like search bar (e.g. with `AJAX` http calls to the API server).

### See the graph

You may also check the GraphDB content on your http://localhost:9000 page.

Password is: `catalogapi`.
