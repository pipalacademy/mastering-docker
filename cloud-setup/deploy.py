from pyinfra.operations import files, server, apt, pip

SRC_PATH = "../mastering-docker.tgz"
DEST_PATH = "/tmp/mastering-docker.tgz"

APT_PACKAGES = """
python3-pip
python-is-python3
python3.11-venv
""".strip().split()

files.put(
    name="Put mastering-docker.tgz",
    src=SRC_PATH,
    dest=DEST_PATH)

server.shell(
    name="extract mastering-docker.tgz",
    commands=["mkdir -p /opt/mastering-docker",
              "tar xvzf /tmp/mastering-docker.tgz --directory /opt/mastering-docker",
              "rm -f /usr/bin/problem-cheker",
              "ln -sf /opt/mastering-docker/scripts/problem-checker /usr/bin/"],
    _sudo=True
)

apt.packages(packages=APT_PACKAGES, _sudo=True)

pip.venv(
    name="Create a virtualenv",
    path="/opt/venv",
    _sudo=True
)
pip.packages(requirements="/opt/mastering-docker/requirements.txt",
             virtualenv="/opt/venv",
            _sudo=True)