# Session 3

## Starting MySQL container

```
$ mkdir mysql
$ cd mysql
$ mkdir data
```

Run mysql server with mouting `data` as the mysql data directory.

```
$ docker run -v $PWD/data:/var/lib/mysql --rm --name mysql -e MYSQL_ROOT_PASSWORD=docker mysql
```

Try connecting to it from another terminal by running:

```
$ docker exec -it mysql  mysql -u root -p
Enter Password:
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.00 sec)

mysql> create database docker;
Query OK, 1 row affected (0.01 sec)

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| docker             |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)
```

You can see that you've created database with name docker.

Try stop the server and see if the database persists after restarting the docker container.

```
$ docker stop mysql
```

And run it again.

```
$ docker run -v $PWD/data:/var/lib/mysql --rm --name mysql -e MYSQL_ROOT_PASSWORD=docker mysql
```

From another terminal connect again:

```
$ docker exec -it mysql  mysql -u root -p
Enter Password:
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| docker             |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)
```

You'll see that the database `docker` is still there.

## Building FastAPI docs using Docker

Clone fastapi if you have not done it already.

```
$ git clone https://github.com/tiangolo/fastapi
```

Build the docs in a docker container.

```
$ cd fastapi

$ $ docker run -it --rm -v $PWD:/app python bash
root@7a053b24a615:/#
root@7a053b24a615:/#
root@7a053b24a615:/# cd /app/
root@7a053b24a615:/app# pip install - requirements-docs.txt
...
root@7a053b24a615:/# cd docs/en
root@7a053b24a615:/# mkdocs build

```

