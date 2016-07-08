
## API catalog *prototype*

Testing REST API development to fill caches of a catalog.

### Data model

* The neomodels mapping of our data into a graph db can be found [here](vanilla/models/neo4j.py).
* The implementation of current endpoints is available at [this python class](vanilla/apis/fedapp.py)

### Pre-requisites for execution

Before starting please make sure that you have installed on your system:

* [Docker](http://docs.docker.com/) 1.12+
* [docker-compose](https://docs.docker.com/compose/) 1.7+


### Run the project

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

# Run the client to create data inside the GraphDB
/code $ python3 register.py
2016-07-07 08:09:05,608 __main__     INFO     POST: received id 'aa90135e-7242-4790-a389-1500b67074a9'
2016-07-07 08:09:06,506 __main__     INFO     PUT: updated. Out = aa90135e-7242-4790-a389-1500b67074a9
2016-07-07 08:09:06,525 __main__     INFO     GET: Hello world

```

You may now check the GraphDB on your http://localhost:9000 page.
Password is: 'catalogapi'
