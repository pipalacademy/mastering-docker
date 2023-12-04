# Running Multi-container Applications

!!! quote

    “Alone we can do so little; together we can do so much.”

    – Helen Keller

Introduction to running multi-container applications with docker-compose.

## Introduction

_Docker Compose_ is a tool for defining and running multi-container applications.

Verify if _Docker Compose_ is installed.

```
$ docker compose version
Docker Compose version v2.21.0
```

## Try Docker Compose

Clone [flask-redis](https://github.com/anandology/flask-redis) repository.

```
$ git clone https://github.com/anandology/flask-redis
...
$ cd flask-redis
```

This is a Flask webapp that uses _Redis_ to store the page view count.

```
$ cat app.py
...
$ cat Dockerfile
...
$ cat compose.yml
...
```

Run this app using docker compose.

```
$ docker compose up
...
```

This will start both the services listed in the `compose.yml` file and the application will be live at `http://alpha.k8x.in:8000/`.

Please open a new terminal, login to the server, cd to the same directory and run the following.

The `docker compose ps` command will show the containers running in this application.

```
$ docker compose ps
NAME                  IMAGE                COMMAND              SERVICE   CREATED              STATUS              PORTS
flask-redis-redis-1   redislabs/redismod   "redis-server ..."   redis     About a minute ago   Up About a minute   6379/tcp
flask-redis-web-1     flask-redis-web      "python3 app.py"     web       About a minute ago   Up About a minute   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp
```

These containers will also appear in the output when you run `docker ps`.

Try accessing the the redis container and reset the hits counter.

```
$ $ docker compose exec redis redis-cli
127.0.0.1:6379> get hits
"13"
127.0.0.1:6379> del hits
(integer) 1
127.0.0.1:6379> get hits
(nil)
```

Now you'll see that the count has been reset.

You can restart a service using:

```
$ docker compose restart service-name
```

You can stop everything using:

```
$ docker compose down
```

You can start the application in the background using:

```
$ docker compose up -d
```

If you want to look at the logs, use:

```
$ docker compose logs
```

Often it is handy to look at the last few entries in the log and follow the new entries.

```
$ docker compose logs --tail 20 -f
```

Try stoping the redis service, access the app from the browser and see what error is shown in the log.

## Graphviz

Let's run graphviz-frontend and graphviz-api using docker-compose.

```
$ cat compose.yml
services:
    frontend:
        build: graphviz-frontend
        ports:
          - 8080:8080
        environment:
          GRAPHVIZ_API_ENDPOINT: "http://alpha.k8x.in:8008/dot"
    api:
        build: graphviz-api
        ports:
          - 8008:8000

$ docker-compose up
...
```

The `docker-compose up` will start both the containers with everything setup.

You should be able to visit `http://alpha.k8x.in:8080/` to visit the graphviz-web.


## Example: Nginx


```
#
# docker run -p 8000:80 -v $PWD/html:/usr/share/nginx/html nginx
#

services:
  web:
    image: "nginx"
    ports:
      - "8000:80"
    volumes:
      - ./html:/usr/share/nginx/html
```

## Example: Gitea with sqlite


```
$ mkdir gitea
$ cd gitea
$ mkdir data config

$ cat compose.yml
services:
  server:
    image: gitea/gitea:1.21.1-rootless
    restart: always
    volumes:
      - ./data:/var/lib/gitea
      - ./config:/etc/gitea
    ports:
      - "3000:3000"
      - "2222:2222"
```

## Example: Gitea with Postgres


## Problem: Saarli

[Shaarli](https://shaarli.readthedocs.io/en/master/) is a minimalist database-free bookmarking service.

Install _Shaarli_ on your server using docker compose.

The docker image of _Shaarli_ is available from `ghcr.io/shaarli/shaarli`.

The docker container uses port `80` and stores the data and cache in `/var/www/shaarli/data` and `/var/www/shaarli/cache` respectively.

Write a `compose.yml` file to run _Shaarli_ on your server and expose it via nginx at `https://links.alpha.k8x.in`.


Make sure you give `o+rwx` permissions to the data and cache directory. This is a work-around to handle the issue that a different user is running in the docker container.

```
$ chmod o+rwx data cache
```

## Tasks

### Setup bookmarks service - links.alpha.k8x.in

Setup [Shaarli][], an opensource bookmarking service using docker-compose at https://links.alpha.k8x.in/.

[Shaarli]: https://shaarli.readthedocs.io/en/master/

### Setup Klickr

Start klickr app on your node.

<https://github.com/pipalacademy/klickr>

### Deploy Etherpad on your instance

See <https://etherpad.org> for details.

Your goal is to setup <http://pad.alpha.k8x.in/>. You may have to use docker-compose to set this up.

You can look at a sample etherpad instance at:
<https://pad.libreops.cc/>

Make sure that your application persists the data. If the docker is restarted, the application data should not be lost.

Etherpad support multiple database engines. Use the simplest one `sqlite` and mount a file from host to use the database file.

When you are configuring nginx, you will have to configure it to handle websockets. Please refer to the nginx documentaion for details.
<https://nginx.org/en/docs/http/websocket.html>