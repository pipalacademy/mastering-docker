# Session 1: Managing a Remote Server

::: {.callout-warning}
This lesson is work in progress.
:::

## Working on remote machines

## Working with files & directories

```
pwd
ls
cat
mkdir
cd
vi
ln
```

## Sudo

![XKCD comic on sudo](https://imgs.xkcd.com/comics/sandwich.png)

## Installing software

apt-get

## sudo

## Writing shell scripts

## Deploying static sites with nginx

### Change the HTML

```bash
$ cd /var/www/html
```

Create `index.html`  with the following text.

```text
hello
```

### Setup hello.alpha.k8x.in {#sec-nginx-hello}

create a file `/etc/nginx/sites-enabled/hello`.

```bash
server {
	listen 80;
	server_name hello.alpha.k8x.in;

	root /var/www/hello;
}
```

And create `/var/www/hello` directory.

```bash
$ mkdir  /var/www/hello
```

And create `index.html` in that directory with the following content.

```html
<pre>
 _          _ _
| |__   ___| | | ___
| '_ \ / _ \ | |/ _ \
| | | |  __/ | | (_) |
|_| |_|\___|_|_|\___/
</pre>
```

And reload nginx.

```
$ sudo service nginx reload
```

Now vist <http://hello.alpha.k8x.in/>.

### python.alpha.k8x.in

Open a new terminal, ssh to the server and run the following command.

```bash
$ python -m http.server
```

create a file `/etc/nginx/sites-enabled/python` with the following content.

```bash
server {
	listen 80;
	server_name python.alpha.k8x.in;

	location / {
		proxy_pass http://localhost:8000/;
	}
}
```

And restart nginx.

```bash
$ sudo service nginx restart
```

Visit <http://python.alpha.k8x.in/>


## Deploy figlet-web

Let's see what does it take to deploy a Python webapp.

We'll deploy a simple webapp `figlet-web`.

Create a new tmux window for setting up the app.

We'll be using the [figlet-web](https://github.com/anandology/figlet-web) app for this.

Start with cloning the repository in your home directory.

```
$ git clone https://github.com/anandology/figlet-web.git
...
$ cd figlet-web
```

Create a virtual env. You may have to install the apt package `python3-venv`, if it is not already installed.

```
$ python3 -m venv venv
...
$ source venv/bin/activate
```

Install the dependencies.

```
$ pip install -r requirements.txt
```

Run the webapp.

```
$ gunicorn -b 0.0.0.0:8000 webapp:app
```

Now your site will be accessible at `http://alpha.k8x.in:8000/`.

### Setting up nginx reverse proxy {#sec-nginx-proxy}

However, it is a good idea to expose guncorn webserver to the outside world directly. It is a good practice to put it behind nginx.

```
Gunicorn <--> Nginx <--> Internet
```

Lets setup `figlet-web.alpha.k8x.in`.

Keep the window with python webapp continue running and open a new window to setup nginx.

Create a new config file `figlet-web` in `/etc/nginx/sites-enabled/` with the following contents.

```
$ cd /etc/nginx/sites-enabled
$ sudo vi figlet-web
server {
    listen 80;
    server_name figlet-web.alpha.k8x.in;
    root /var/www/figlet-web;

    location / {
        proxy_pass http://localhost:8000/;
    }
}
```

The `proxy_pass` directive passes all the requests to the gunicorn service.

## Setting up HTTPS {#sec-letsencrypt}

Lets install certbot to get https certificates.

```
$ sudo apt install certbot python3-certbot-nginx
```

Now it is time to get https certificates from certbox.

```
$ sudo certbot --nginx
```

And follow the instructions!

## Configuring a Service with Systemd {#sec-systemd-service}

create a file `/etc/systemd/system/figlet-web.service`

```bash
[Unit]
Description=figlet-web service
After=network.target

[Service]
User=pipal
WorkingDirectory=/home/pipal/figlet-web
ExecStart=/home/pipal/figlet-web/venv/bin/gunicorn -b 127.0.0.1:8000 webapp:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Reload systemd.

```
$ sudo systemctl daemon-reload
```

Start the service.

```
$ sudo service figlet-web start
```

## Assignment

### Problem 1: Build & Deploy FastAPI docs

[FastAPI](https://fastapi.tiangolo.com/) is a modern web framework in Python.

The source code and documentation of the framework is available in the following git repository.

<https://github.com/tiangolo/fastapi>

Your task is to build the docs and deploy it at `https://fastapi.alpha.k8x.in/`.

**How to build**

Step 1: Clone the repo

```bash
$ git clone https://github.com/tiangolo/fastapi
$ cd fastapi
```

Step 2: setup a virtual env & install dependencies to build the docs

```bash
$ python -m venv
$ source venv/bin/activate
$ pip install -r requirements-docs.txt
```

Step 3: Build the docs

```bash
$ cd docs/en
$ mkdocs build
```

The documentation is built in `site/` directory.

Step 4: Symlink the docs to /var/www/fastapi

Symlink the generated docs to `/var/www/fastapi` so that you can serve it from nginx.

```bash
$ sudo ln -s /home/pipal/fastapi/docs/en/site /var/www/fastapi
```

Verify the symlink.

```bash
$ ls -l /var/www/fastapi
lrwxrwxrwx 1 root root 32 Nov 17 07:09 /var/www/fastapi -> /home/pipal/fastapi/docs/en/site
```

**Explosing the site on nginx**

Create a new configuation file with `/etc/nginx/sites-enabled/fastapi` to server `/var/www/fastapi` at domain `fastapi.alpha.k8x.in`.

Please refer to @sec-nginx-hello for instructions.

**Setting up HTTPS**

Setup HTTPS for this domain using the instructions given in @sec-letsencrypt.

::: {.callout-note}
Please remember to replace `alpha` with your hostname in the domain name.

If you hostname is `beta`, then domain name to deploy will be `fastapi.beta.k8x.in`.
:::

### Problem 2: Deploy the railways data as datasette website

[Datasette](https://datasette.io) is a tool for exploring and publishing data.

Use _Datasette_ to publish the indian railways data as a website at `https://railways.alpha.k8x.in/`.

**Usage**

Step 1: clone the repo

```bash
$ git clone https://github.com/anandology/railways
$ cd railways
```

Step 2: Create a sqlite3 database

```bash
$ sqlite3 railways.db < schema.sql
$ sqlite3 railways.db < import.sql
```

You may have to install apt package `sqlite3` before doing this.

Step 3: Setup a virtualenv and install dependencies

Create a virtualenv.

```bash
$ python -m venv venv
$ source venv/bin/activate
```

Install `datasette`.

```bash
$ pip install datasette
```

Step 4: Serve the dataset using datasette

```bash
$ datasette serve --ip 0.0.0.0 --port 8000 railways.db
```

You'll be able to access it from `http://alpha.k8x.in:8000/`.

You can use a different port number if the port 8000 is already in use.

**Deployment**

For deploying, you need to setup the datasette as a system service. See @sec-systemd-service for instructions.

You need to setup an nginx site `railways.alpha.k8x.in` proxying the datasette port. See @sec-nginx-proxy for instuctions.

You also need to setup HTTPS for this site. Please refer to @sec-letsencrypt for instructions.

Please rememeber that you may not want to run the datasette server on `0.0.0.0` in production as show in the instructions above. The above instructions are for you to get it running and accessing it directly from outside. However, when you deploy in production, you would want the app to be accessible only via nginx. The good practice is to not run the service on `0.0.0.0`. Do that by skipping `--ip 0.0.0.0` in the command when you setup systemd service.

```bash
$ datasette serve --port 8000 railways.db
```

::: {.callout-note}
Please remember to replace `alpha` with your hostname in the domain name.

If you hostname is `beta`, then domain name to deploy will be `railways.beta.k8x.in`.
:::

