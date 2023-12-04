
default: docs

push:
	tar czf mastering-docker.tgz problems/ scripts/ requirements.txt
	cd cloud-setup && pyinfra inventory.py deploy.py

docs:
	mkdocs build
	rsync -avz site/* docker.pipal.in:/var/www/docker.pipal.in/
