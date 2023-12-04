# Assignment 1

Due Date: Tue Nov 21, 2023 - 11:59 PM

## Problem 1: Build & Deploy FastAPI docs

[FastAPI](https://fastapi.tiangolo.com/) is a modern web framework in Python.

The source code and documentation of the framework is available in the following git repository.

<https://github.com/tiangolo/fastapi>

Your task is to build the docs and deploy it at `https://fastapi.alpha.k8x.in/`.

### How to build

**Step 1: Clone the repo**

```
$ git clone https://github.com/tiangolo/fastapi
$ cd fastapi
```

**Step 2: setup a virtual env & install dependencies to build the docs**

```
$ python -m venv
$ source venv/bin/activate
$ pip install -r requirements-docs.txt
```

**Step 3: Build the docs**

```
$ cd docs/en
$ mkdocs build
```

The documentation is built in `site/` directory.

**Step 4: Symlink the docs to /var/www/fastapi**

Symlink the generated docs to `/var/www/fastapi` so that you can serve it from nginx.

```
$ sudo ln -s /home/pipal/fastapi/docs/en/site /var/www/fastapi
```

Verify the symlink.

```
$ ls -l /var/www/fastapi
lrwxrwxrwx 1 root root 32 Nov 17 07:09 /var/www/fastapi -> /home/pipal/fastapi/docs/en/site
```

### Explosing the site on nginx

Create a new configuation file with `/etc/nginx/sites-enabled/fastapi` to server `/var/www/fastapi` at domain `fastapi.alpha.k8x.in`.

Please refer to [this section](../../session1/#sec-nginx-hello) for instructions.

### Setting up HTTPS

Setup HTTPS for this domain using the instructions given in [Setting up HTTPS](../../session1/#sec-letsencrypt).

!!! note

    Please remember to replace `alpha` with your hostname in the domain name.

    If you hostname is `beta`, then domain name to deploy will be `fastapi.beta.k8x.in`.

## Problem 2: Deploy the railways data as datasette website

[Datasette](https://datasette.io) is a tool for exploring and publishing data.

Use _Datasette_ to publish the indian railways data as a website at `https://railways.alpha.k8x.in/`.

### Usage

**Step 1: clone the repo**

```
$ git clone https://github.com/anandology/railways
$ cd railways
```

**Step 2: Create a sqlite3 database**

```
$ sqlite3 railways.db < schema.sql
$ sqlite3 railways.db < import.sql
```

You may have to install apt package `sqlite3` before doing this.

**Step 3: Setup a virtualenv and install dependencies**

Create a virtualenv.

```
$ python -m venv venv
$ source venv/bin/activate
```

Install `datasette`.

```
$ pip install datasette
```

**Step 4: Serve the dataset using datasette**

```
$ datasette serve --host 0.0.0.0 --port 8000 railways.db
```

You'll be able to access it from `http://alpha.k8x.in:8000/`.

You can use a different port number if the port 8000 is already in use.

### Deployment

For deploying, you need to setup the datasette as a system service. See [Systemd Services](../../session1/#sec-systemd-service) for instructions.

You need to setup an nginx site `railways.alpha.k8x.in` proxying the datasette port. See [Setting up nginx reverse proxy](../../session1/#sec-nginx-proxy) for instuctions.

You also need to setup HTTPS for this site. Please refer to [Setting up HTTPS](../../session1/#sec-letsencrypt) for instructions.

Please rememeber that you may not want to run the datasette server on `0.0.0.0` in production as show in the instructions above. The above instructions are for you to get it running and accessing it directly from outside. However, when you deploy in production, you would want the app to be accessible only via nginx. The good practice is to not run the service on `0.0.0.0`. Do that by skipping `--host 0.0.0.0` in the command when you setup systemd service.

```
$ datasette serve --port 8000 railways.db
```

!!! note

    Please remember to replace `alpha` with your hostname in the domain name.

    If you hostname is `beta`, then domain name to deploy will be `railways.beta.k8x.in`.
