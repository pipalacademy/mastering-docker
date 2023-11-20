# Publishing Ports

Docker allows to publish a port in the container to the host.

```
$ docker run -p 8080:80 nginx
...
```

That would run nginx and publish the port 80 of the container to port 8080 of the host. After doing this, you'll be able to access it at http://alpha.k8x.in:8080/ (replace alpha with your hostname).

**Problem:** Nginx docker image serves the index.html file from `/usr/share/nginx/html`. Create a new docker image nginx-hello-docker that serves a page showing the following:

```
 _   _      _ _         ____             _             _
| | | | ___| | | ___   |  _ \  ___   ___| | _____ _ __| |
| |_| |/ _ \ | |/ _ \  | | | |/ _ \ / __| |/ / _ \ '__| |
|  _  |  __/ | | (_) | | |_| | (_) | (__|   <  __/ |  |_|
|_| |_|\___|_|_|\___/  |____/ \___/ \___|_|\_\___|_|  (_)

```

Hint: You may have to write a `Dockerfile`.

## Example: A python webapp <a name="figlet-web"></a>

Let's try to build a docker image for packaging a python webapp.

We'll use [figlet-web](https://gitub.com/anandology/figlet-web), a simple webapp that exposes `figlet` as a webapp for this exercise.

The README file in the repository has all the instructions on how to install it.

There will be slight changes when we convert those into a Docker file.

First, start the `Dockerfile` with python base image.

```
FROM python
```

Then we need to install apt package `figlet`.

```
RUN apt-get update
RUN apt-get install figlet
```

Then we need to add all the code to the docker container.

```
ADD . /app
```

We better make this our work directory so that all the commands we run from now on will happen here.

```
WORKDIR /app
```

Next step is to install the dependencies.

```
RUN pip install -r requirements.txt
```

Finally, the command to run as specified in the README.

```
CMD ["gunicorn", "-b", "0.0.0.0:8000", "webapp:app"]
```

If we put all of these together in the `Dockerfile`

```
FROM python
RUN apt-get update
RUN apt-get install -y figlet
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["gunicorn", "-b", "0.0.0.0:8000", "webapp:app"]
```

Please note that we were able to run `apt-get` as part of build because the base image of python was build with a base image of Debian/Ubuntu. If that was not the case, we may have to do it in a different way.

Now, build the docker image:

```
$ docker build . -t figlet-web
```

And run it, exposing port `8000`.

```
$ docker run --rm -p 8000:8000 figlet-web
```

## Exercise: Graphviz-web

Clone the git repository containing code samples.

```
$ git clone https://github.com/pipalacademy/graphviz-web/
```

Task 1: Build an image for `graphviz-frontend` and run it as a container. The instructions are specified in the README.md file in graphviz-frontend directory.

At the end of this exercise, it should be possible to access it from your browser.

Task 2: Run `graphviz-api` as a contaner. The instructions are avalilable in README.md file in graphviz-api directory.

At the end of this exercise, you should be able to access the API using curl as shown in the README.

Task 3: Configure graphviz-web to talk to the graphviz-api instance. Instructions are again in the `README.md` of graphviz-web.

At the end of this exercise, clicking on "generate" should show the resulting image on the right.


Hints:

```
$ cd graphviz-frontend
$ docker run -it -p8080:8080 -v $PWD:/app golang
root@e1df1e009486:/go# cd /app/
root@e1df1e009486:/app# go build web.go
root@e1df1e009486:/app# ./web
2022/03/17 11:07:39 Starting the server...

$ cat Dockerfile
FROM golang
ADD . /app
WORKDIR /app
RUN go build web.go
CMD ["/app/web"]
```