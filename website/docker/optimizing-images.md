# Optimizing Docker Images

## Pin version of docker images

For example, when building image for a python app:

```
FROM python:3.10
...
```

The image `python` is a short hand for `python:latest`, which keep changing to the latest version whenever a new version of python docker image is built. That forces our docker image to be rebuilt as the base image has changed.

It is good practice to pin the version of base image.

## Using tags to version docker images

As we make changes to docker images, it is important to maintain backward compatability. One good way to achieve that is to tag the images with version.

The figlet image that we have built in this course had three versions.

### Figlet 0.1

The Figlet 0.1 just printed "hello world"

```
FROM ubuntu

# run apt-get update and apt-get install commands as part of the build
RUN apt-get update
RUN apt-get -y install figlet

# When running the container, use the following as the default command
CMD ["figlet", "hello docker"]
```

We could build that as tag it as `figlet:0.1` and also as `figlet:latest`.

```
$ docker build . -t figlet -t figlet:0.1
...
```

Now we can see the images.

```
$ docker images figlet
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
figlet       0.1       264bd955727a   6 seconds ago    125MB
figlet       latest    264bd955727a   6 seconds ago    125MB
```

### Figlet 0.2

We have an entrypoint in 0.2.

```
$ cat Dockerfile
FROM ubuntu
RUN apt-get update
RUN apt-get -y install figlet
ENTRYPOINT ["figlet"]
CMD ["hello docker"]
```

We can build this with tag `0.2`. It is a good practice to update the `latest` whenever a new version is built.

```
$ docker build . -t figlet:0.2 -t figlet
...
```

The images now will include `0.2` tag.

```
$ docker images figlet
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
figlet       0.2       7be43df61825   4 minutes ago    125MB
figlet       latest    7be43df61825   4 minutes ago    125MB
figlet       0.1       264bd955727a   4 minutes ago    125MB
```

### Figlet 0.3

In next version we've added a shell script that looks for environment variable FONT.

```
$ cat figlet.sh
#! /bin/bash

# use $FONT if defined, else use "standard"
FIGLET_FONT=${FONT:-standard}
figlet -f $FIGLET_FONT $*

$ chmod +x figlet.sh

$ cat Dockerfile
FROM ubuntu

RUN apt-get update
RUN apt-get install -y figlet

ADD figlet.sh /

ENTRYPOINT ["/figlet.sh"]
CMD ["hello world"]
```

Build version `0.3`.

```
$ docker build . -t figlet:0.3 -t figlet
...
```

Now the latest image will be same as `0.3`.

```
$ docker images figlet
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
figlet       0.3       a7d55de3aa69   2 seconds ago    125MB
figlet       latest    a7d55de3aa69   2 seconds ago    125MB
figlet       0.1       264bd955727a   9 minutes ago    125MB
figlet       0.2       7be43df61825   9 minutes ago    125MB
```

## Understanding Layers

A docker image is made of multiple layers.

We can find all the layers of an image using `docker history`.

```
$ docker history figlet
$ docker history figlet
IMAGE          CREATED              CREATED BY                                      SIZE      COMMENT
a7d55de3aa69   About a minute ago   CMD ["hello docker"]                            0B        buildkit.dockerfile.v0
<missing>      About a minute ago   ENTRYPOINT ["/figlet.sh"]                       0B        buildkit.dockerfile.v0
<missing>      About a minute ago   ADD figlet.sh / # buildkit                      115B      buildkit.dockerfile.v0
<missing>      9 days ago           RUN /bin/sh -c apt-get install -y figlet # b…   1.56MB    buildkit.dockerfile.v0
<missing>      10 days ago          RUN /bin/sh -c apt-get update # buildkit        45.8MB    buildkit.dockerfile.v0
<missing>      8 weeks ago          /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
<missing>      8 weeks ago          /bin/sh -c #(nop) ADD file:63d5ab3ef0aab308c…   77.8MB
<missing>      8 weeks ago          /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B
<missing>      8 weeks ago          /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B
<missing>      8 weeks ago          /bin/sh -c #(nop)  ARG LAUNCHPAD_BUILD_ARCH     0B
<missing>      8 weeks ago          /bin/sh -c #(nop)  ARG RELEASE                  0B
```

We can see how much each step in the Dockerfile is contributing to the image size.

In the above example, installing figlet is adding only `1.56MB`, but doing `apt-get update` is contributing more than `45 MB`. This is something that can be avoided with some tricks.

## Optimizing Docker Images

Here are some tricks to optimize docker images.

Also see [Best practices for Dockerfile instructions][1] from Docker docs.

[1]: https://docs.docker.com/develop/develop-images/instructions/

### Use Alpine Images when possible

_Alpine_ is a lightweight Linux distribution and doesn't come with many binaries that are shipped with common distibutions like Ubuntu.

The base image of Alpine is about 7 MB while the base image of Ubuntu is 70 MB.

```
$ docker images ubuntu
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
ubuntu       latest    e4c58958181a   8 weeks ago   77.8MB

$ docker images alpine
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
alpine       latest    8ca4688f4f35   2 months ago   7.34MB
```

While ubuntu uses `apt` for installing packages, alpine used `apk` for installing packages.

Let's try to build Figlet alpine image.

```
$ cat Dockerfile.alpine
FROM alpine
RUN apk add figlet
CMD ["figlet", "hello docker"]

$ docker build . -t figlet:alpine -t figlet:0.1-alpine -f Dockerfile.alpine
...

$ docker run figlet:alpine
 _          _ _             _            _
| |__   ___| | | ___     __| | ___   ___| | _____ _ __
| '_ \ / _ \ | |/ _ \   / _` |/ _ \ / __| |/ / _ \ '__|
| | | |  __/ | | (_) | | (_| | (_) | (__|   <  __/ |
|_| |_|\___|_|_|\___/   \__,_|\___/ \___|_|\_\___|_|


$ docker images figlet
REPOSITORY   TAG          IMAGE ID       CREATED          SIZE
figlet       0.1-alpine   8f2235b9599e   3 seconds ago    9.89MB
figlet       alpine       8f2235b9599e   3 seconds ago    9.89MB
figlet       0.3          a7d55de3aa69   16 minutes ago   125MB
figlet       latest       a7d55de3aa69   16 minutes ago   125MB
figlet       0.1          264bd955727a   26 minutes ago   125MB
figlet       0.2          7be43df61825   26 minutes ago   125MB
```

As you can see the new docker image is less than 10MB while the intial one was more than 100MB.

Most of the popular images build an alpine version as well. Try to use the alpine version whenever possible. For example, use `nginx:alpine` instead of `nginx`.

There will be cases when you need to install an `apt` package as that is not available in the Apline world with `apk`. In such cases we'll not be able to use alpine images.

Any standard images also provide a stripped down version of the image based on Debian/Ubuntu with tag `slim`. Checkout that option if alpine doesn't work for your use case.

#### Problem: graphviz-frontend:alpine

Switch graphviz-frontend to alpine and see the difference in the file size.

See <https://github.com/pipalacademy/graphviz-web> for details.

### Optimizing apt-get

Each command that we add to the Dockerfile will add a new layer. When we are installing something with `apt-get` it is a good practice to update and install as a single command and cleanup at the end.

Remember the `apt-get update` step of `figlet` contributed to about 45MB to the image size. When we run `apt-get update`, it maintains the list of packages in `/var/lib/apt/lists`, which is required for `apt-get install`, but there is no use after that. We could address that by running both commands in the same `RUN` step and delete those files at the end.

```
FROM ubuntu

RUN apt-get update \
    && apt-get install -y figlet \
    && rm -rf /var/lib/apt/lists/*
CMD ["figlet", "hello docker"]
```

Lets build this and see the image size.


```
$ docker build . -t figlet:0.1.1
...

$ docker images figlet:0.1.1
REPOSITORY   TAG       IMAGE ID       CREATED              SIZE
figlet       0.1.1     ff5f8df6aefa   About a minute ago   79.4MB
```

As you can see the image size has come down from 125 MB to 80 MB.

```
$ docker history figlet:0.1.1
IMAGE          CREATED              CREATED BY                                      SIZE      COMMENT
ff5f8df6aefa   About a minute ago   CMD ["figlet" "hello docker"]                   0B        buildkit.dockerfile.v0
<missing>      About a minute ago   RUN /bin/sh -c apt-get update     && apt-get…   1.56MB    buildkit.dockerfile.v0
<missing>      8 weeks ago          /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
<missing>      8 weeks ago          /bin/sh -c #(nop) ADD file:63d5ab3ef0aab308c…   77.8MB
<missing>      8 weeks ago          /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B
<missing>      8 weeks ago          /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B
<missing>      8 weeks ago          /bin/sh -c #(nop)  ARG LAUNCHPAD_BUILD_ARCH     0B
<missing>      8 weeks ago          /bin/sh -c #(nop)  ARG RELEASE                  0B
```

As you can see the 45MB overhead is gone and we are just adding 1.56 MB for figlet command on top of the base image. Pretty neat, isn't it?

#### Problem: graphviz-api

Build the following three versions of Docker image for graphviz-api.

optimized: Update the graphviz-api Dockerfile to optimize apt-get install.

alpine: use alpine image and see if it work.

slim: use the `python:slim` image and see if that works.

What is the image size for all these three versions?


### The Instruction Order

The order of instructions makes a difference in the time it takes to build a docker image. It is important to write Dockerfiles in a way that builds reuse layers from docker build cache as much as possible. While this may not change the size of the image, it affects the time taken to build quite a lot.

Docker maintaians a build cache of intermmediate layers and reuses them if it identifies that nothing has changed in the build context that requires a fresh build of a layer. However, every later depends on the layer above and if one layer changes, everything below it is required to be rebuilt. So it is better to move the items that most likely to change towards the end of the Docker file.

Consider this Dockerfile for figlet-web.

```
$ cat Dockerfile
FROM python
ADD . /app
WORKDIR /app
RUN apt-get update \
    && apt-get install -y figlet \
    && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
CMD ["gunicorn", "-b", "0.0.0.0:8000", "webapp:app"]
```

It adding the entire application to `/app` as the first step of the `Dockerfile`. If file changes in the app, even if you add a comment to the `Dockerfile`, that command and everything below it needs to be rebuilt. As you can see the `apt-get` doesn't really depend on any code in the directory. It is better to move that to the top so that we cache that part and don't have to pay that time for every build.

```
FROM python
RUN apt-get update \
    && apt-get install -y figlet \
    && rm -rf /var/lib/apt/lists/*
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["gunicorn", "-b", "0.0.0.0:8000", "webapp:app"]
```

That is a lot better, but we could do even better. Why do we have to reinstall pip packages if we change a source file or a Dockerfile? Wouldn't it be nice to move that also to the top? But that requires a file in the current directory, the `requirements.txt`. The trick is to add only that file first to the image and postpone adding all other files until the end.

```
FROM python
RUN apt-get update \
    && apt-get install -y figlet \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
ADD requirements.txt /app
RUN pip install -r requirements.txt
ADD . /app
CMD ["gunicorn", "-b", "0.0.0.0:8000", "webapp:app"]
```

### Multi-stage Build

Docker supports multi-stage builds where we build the application in one stage and copy the relevant files to another stage.

Lets try 3 different Dockerfiles for the graphviz-frontend application.

Regular approach.

```
$ cat Dockerfile
FROM golang
WORKDIR /app
ADD . /app
RUN go build web.go
CMD ["/app/web"]

$ docker build . -t graphviz-frontend
...
$ docker images graphviz-frontend
REPOSITORY     TAG           IMAGE ID       CREATED         SIZE
graphviz-frontend   latest        3d41119392fc   23 hours ago    977MB
```

Using an alpine image.

```
$ cat Dockerfile.alpine
FROM golang:alpine
WORKDIR /app
ADD . /app
RUN go build web.go
CMD ["/app/web"]

$ docker build . -t graphviz-frontend:alpine -f Dockerfile.alpine
...
$ docker images graphviz-frontend
REPOSITORY     TAG           IMAGE ID       CREATED         SIZE
graphviz-frontend   alpine        f3dec315884d   9 minutes ago   342MB
graphviz-frontend   latest        3d41119392fc   23 hours ago    977MB
```

Let's try a multi-stage build now.

```
$ cat Dockerfile.multi-stage
FROM golang:alpine
WORKDIR /app
ADD . /app
RUN go build web.go

FROM alpine
WORKDIR /app
COPY --from=0 /app /app
CMD ["/app/web"]

$ docker build . -t graphviz-frontend:multi-stage -f Dockerfile.multi-stage
...
$ docker images graphviz-frontend
REPOSITORY     TAG           IMAGE ID       CREATED         SIZE
graphviz-frontend   multi-stage   8c37ac3ee317   4 minutes ago   11.9MB
graphviz-frontend   alpine        f3dec315884d   9 minutes ago   342MB
graphviz-frontend   latest        3d41119392fc   23 hours ago    977MB
```

#### Problem: Multi-stage build for fastAPI docs

Write a multi-stage Dockerfile to build the docs of FastAPI in a Python container and then copy the over to `nginx:alpine`.

See [Assignment 1](https://docker.pipal.in/assignments/assignment-1/) for instructions on how to build this.

Hints:

* The nginx container serves the files from `/usr/share/nginx/html`.
* The nginx container runs on port 80