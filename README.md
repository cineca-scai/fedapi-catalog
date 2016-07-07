
## API catalog *prototype*

Testing REST API development to fill caches of a catalog.


### Pre-requisites

Before starting please make sure that you have installed on your system:

* [Docker](http://docs.docker.com/) 1.12+
* [docker-compose](https://docs.docker.com/compose/) 1.7+


### Check the project

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

# Check if the server is reachable
$ ./do client_shell

/code # http apiserver/api/status
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
Connection: keep-alive
Content-Length: 19
Content-Type: application/json
Date: Thu, 07 Jul 2016 08:05:00 GMT
Server: nginx/1.11.1

"Server is alive!"

# Run the client to create data inside the GraphDB

/code # python3 register.py
2016-07-07 08:09:05,608 __main__     INFO     POST: received id 'aa90135e-7242-4790-a389-1500b67074a9'
2016-07-07 08:09:06,506 __main__     INFO     PUT: updated. Out = aa90135e-7242-4790-a389-1500b67074a9
2016-07-07 08:09:06,525 __main__     INFO     GET: Hello world

```

You may now check the GraphDB on your http://localhost:9000 page.
Password is: 'catalogapi'
