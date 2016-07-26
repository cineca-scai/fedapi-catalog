
## API catalog *prototype*

Testing REST API development to fill caches of a catalog.


### Data model

* The neomodels mapping of our data into a graph db can be found [here](vanilla/models/neo4j.py).
* The DSL models for elasticsearch indexes can be found [inside this file](vanilla/models/elasticsearch.py)
* The implementation of current endpoints is available at [this python class](vanilla/apis/fedapp.py)


### Pre-requisites

Before starting please make sure that you have installed on your system:

* [Docker](http://docs.docker.com/) 1.11+
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


### Query the REST API server

We may query the server from a client container

```bash
# Open a client container
$ ./do client_shell

# Check if the server is reachable
/code $ http apiserver/api/status
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
Connection: keep-alive
Content-Length: 19
Content-Type: application/json
Date: Thu, 07 Jul 2016 08:05:00 GMT
Server: nginx/1.11.1

"Server is alive!"
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

To be written

### See the graph

You may now check the GraphDB on your http://localhost:9000 page.
Password is: `catalogapi`.
