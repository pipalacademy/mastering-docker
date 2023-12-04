# Assignment 3

## Problem 1: Etherpad

Deploy [Etherpad](https://etherpad.org) on your node running at `https://etherpad.alpha.k8x.in/`.

### Running with Docker

You can run docker container using:

```
$ docker run --rm --detach --name etherpad -p 9001:9001 etherpad/etherpad
```

That would run the docker container on port 9001.

The `--detach` option will run the container in the background.

You can see the container running using:

```
$ docker ps
```

and can stop it using:

```
$ docker stop etherpad
```

### Data Volume

However, if you want to persist the data across restarts, you need to specify the data volume.

```
$ mkdir etherpad
$ cd etherpad
$ mkdir data
$ chmod o+rw data
```

The last step allows other users to read and write the `data` directoty. That is required to allow the etherpad container to write to that directory.

Now run docker container with `data` as volumne.

```
$ docker run --rm --detach --name etherpad -p 9001:9001 -v $PWD/data:/opt/etherpad-lite/var etherpad/etherpad
```

Visit `http://alpha.k8x.in:9001/` to access the site.

You may want to use `-e TRUST_PROXY=true` when you are running etherpad behing nginx proxy.

### Setting up Nginx Proxy

Use the following configuration to setup nginx to proxy to etherpad.

```
server {
    listen       80;
    server_name  etherpad.alpha.k8x.in;

    location / {
        proxy_pass         http://127.0.0.1:9001;
        proxy_buffering    off; # be careful, this line doesn't override any proxy_buffering on set in a conf.d/file.conf
        proxy_set_header   Host $host;
        proxy_pass_header  Server;

        # Note you might want to pass these headers etc too.
        proxy_set_header    X-Real-IP $remote_addr; # https://nginx.org/en/docs/http/ngx_http_proxy_module.html
        proxy_set_header    X-Forwarded-For $remote_addr; # EP logs to show the actual remote IP
        proxy_set_header    X-Forwarded-Proto $scheme; # for EP to set secure cookie flag when https is used
        proxy_http_version  1.1; # recommended with keepalive connections

        # WebSocket proxying - from https://nginx.org/en/docs/http/websocket.html
        proxy_set_header  Upgrade $http_upgrade;
        proxy_set_header  Connection $connection_upgrade;
    }
}


# we're in the http context here
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}
```

### Setting up HTTPS

Follow the instructions in [Setting up HTTPS](https://docker.pipal.in/session1/#setting-up-https) to setup https for this site.

### References

* <https://etherpad.org/>
* <https://github.com/ether/etherpad-lite/blob/develop/doc/docker.adoc>
* <https://github.com/ether/etherpad-lite/wiki/How-to-put-Etherpad-Lite-behind-a-reverse-Proxy#nginx>
