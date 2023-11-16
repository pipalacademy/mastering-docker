from pyinfra.operations import files, server

DOWNLOAD_URL = "https://anandology.com/tmp/mastering-docker.tgz"
DOWNLOAD_PATH = "/tmp/mastering-docker.tgz"

files.download(
    name="Download the mastering-docker.tgz",
    src=DOWNLOAD_URL,
    dest=DOWNLOAD_PATH)

server.shell(
    name="extract mastering-docker.tgz",
    commands=["mkdir -p /opt/mastering-docker",
              "tar xvzf /tmp/mastering-docker.tgz --directory /opt/mastering-docker"],
    _sudo=True
)