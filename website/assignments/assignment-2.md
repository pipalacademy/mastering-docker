# Assignment 2

Due Date: Thu Nov 23, 2023 - 11:59 PM

## Problem 1

Follow the instructions in [Packaging a python app](../../ports/#figlet-web) to run figlet-web as a docker container.

You can run the docker container in the background using the flag `-d`.

```
$ docker run --rm -d -p 8008:8000 figlet-web
```

We are exposing the port 8000 from the container to port 8008 to the host.

Once you run it, it should be accessible from `http://alpha.k8x.in:8008/`.

Expose that via nginx at hostname `figlet-web-docker.alpha.k8x.in` and setup https.

Once everything is done, it should be live at `https://figlet-web-docker.alpha.k8x.in/`

### Hints

If you ever want to remove the container:

* Run `docker ps`
* Look for figlet-web in the output  and find the CONTAINER ID
* Run `docker stop <container-id>`

## Problem 2

Deploy the railways database used in the assignment 1 as datasette service using docker.

Repo: https://github.com/anandology/railways


**Step 1: Create a sqlite3 database**

Create a sqlite database when building the docker image.

```
$ sqlite3 railways.db < schema.sql
$ sqlite3 railways.db < import.sql
```

You may have to install apt package `sqlite3` before doing this.

**Step 2: Install `datasette`**

```
$ pip install datasette
```

**Step 3: Serve the dataset using datasette**

```
$ datasette serve --host 0.0.0.0 --port 8000 railways.db
```

### Your tasks

* Build the docker image and push it to registry as `registry.k8x.in/railways-alpha`
* Run the docker container exposing port 8091 on the host
* Proxy it from nginx serving host `railways-docker.alpha.k8x.in`
* Setup https
