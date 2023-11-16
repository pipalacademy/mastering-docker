"""Fabric script to generate the kubeconfig files and copy them to all nodes.
"""
from __future__ import print_function
import os
import sys
import json
import os
from fabric import SerialGroup

hosts = [line.strip() for line in open("hosts.txt") if line.strip()]
password = os.getenv("PASSWORD")

conn = SerialGroup(*hosts, user="pipal", connect_kwargs={"password": password})

def hello(conn):
    conn.run("echo hello world!")
    conn.run("hostname")

hello(conn)