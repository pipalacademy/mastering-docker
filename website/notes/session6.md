# Session 6

## Problem 1: Build Mastering Docker website

The website for the _Mastering Docker_ course is built using the following git repisitory. It has instructions to build the docs.

https://github.com/pipalacademy/mastering-docker

Write a multi-stage docker file to build these docs and add them to an nginx base image.

Build the image and run in on port 9061. The website should be accessible from `http://alpha.k8x.in:9061/`.

Hints:

* You can use `docker run -d` to run the container in the background.

## Problem 2: Klickr

Klickr is a simple multi-container application like Flickr. It allows users to upload images and see them.

It has a webapp and a worker written in python. Both use the same image. These require Postgres as database and redis as task queue.

Start klickr app on your node.

<https://github.com/pipalacademy/klickr>



