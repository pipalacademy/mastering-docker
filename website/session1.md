# Session 1: Managing a Remote Server

!!! warning

	This lesson is work in progress.


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

### Setup hello.alpha.k8x.in <a name="sec-nginx-hello"></a>

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

### Setting up nginx reverse proxy <a name="sec-nginx-proxy"></a>

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

## Setting up HTTPS <a name="sec-letsencrypt"></a>

Lets install certbot to get https certificates.

```
$ sudo apt install certbot python3-certbot-nginx
```

Now it is time to get https certificates from certbox.

```
$ sudo certbot --nginx
```

And follow the instructions!

## Configuring a Service with Systemd <a name="sec-systemd-service"></a>

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

See [Assignment 1](../assignments/assignment-1/).
