# Assignment 4

## Problem 1

Deploy [streamlit cheatsheet][1] on your server using docker compose.

It is a Python application with dependencies specified in `requirements.txt`. The dependencies can be installed using:

```
$ pip install -r requirements.txt
```

The application can be run using:

```
$ export STREAMLIT_SERVER_PORT=8000
$ streamlit run app.py
```

Write a `Dockerfile` and `compose.yml` to run the Streamlit Cheatsheet app.

Your Tasks:

- Expose the app on port `9041` on your server
- Setup nginx to proxy `streamlit-cheatsheet.alpha.k8x.in` to port `9041`. Please remember Streamkut requires websocket support. See [Nginx docs][2] for websocket configuration.
- Setup HTTPS for the domain

[1]: https://github.com/daniellewisdl/streamlit-cheat-sheet
[2]: https://www.nginx.com/blog/websocket-nginx/

## Problem 2

Setup a private docker registry on your server.

The following tutorial has the instructions to setup this.

<https://www.digitalocean.com/community/tutorials/how-to-set-up-a-private-docker-registry-on-ubuntu-22-04>

* Setup registry running on the your server and expose it at <https://registry.alpha.k8x.in/>.
* Setup authentication with username `pipal` and password `docker`
* Push hello-world image to your registry (see instructions below).

### Pushing hello-world image

After it is set up, you should be able to push and pull images from it.

```
$ docker login registry.alpha.k8x.in
Username: pipal
Password: docker

$ docker pull hello-world
$ docker tag hello-world registry.alpha.k8x.in/hello-world
$ docker push registry.alpha.k8x.in/hello-world
```

Remove the image from the node.

```
$ docker rmi registry.alpha.k8x.in/hello-world
```

Try runing it.

```
$ docker run registry.alpha.k8x.in/hello-world
Unable to find image 'registry.k8x.in/hello-world:latest' locally
latest: Pulling from hello-world
...
```

