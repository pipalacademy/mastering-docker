# Docker Cheatsheet

## Containers

### Run a container

Run a container.

```
docker run image-name
```

Run a container in the background.

```
docker run -d image-name
```

Run a contaner and remove it after it is done.

```
docker run --rm image-name
```

Run a container and get interactive terminal.

```
docker run -it image-name
```




### List running containers

```
docker ps
```

### List all containers

```
docker ps -a
```

### Stop a container

```
docker stop container-id-or-name
```

### Remove a container

To remove a stopped contianer:

```
docker stop container-id-or-name
```

To stop and remove a running container, pass `--force` or `-f` option.

```
docker rm -f container-id-or-name
```

## Images

### List Images

```
docker images
```

### Pull an Image

```
docker pull image-name:optional-tag
```

### Remove an image

```
docker rmi image-name:optional-tag
```

## Environment

### Set an Environment Variable

To set an environment variable when running a container:

```
docker run -e VAR_NAME=value image
```

## Networking

### Expose a port

```
docker run -p host-port:container-port image
```

## Volumes

### Expose a host directory as a volume

```
docker run -v host-directory:container-directory image
```

### Expose current directory as a volume

```
docker run -v $PWD:/container-path image
```

## Troubleshooting

### Run a command inside a running container

```
docker exec -it container-name command
```

### Inspect a container

```
docker inspect containter-name
```
