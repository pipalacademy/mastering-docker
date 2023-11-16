

push:
	tar czf mastering-docker.tgz problems/ scripts/ requirements.txt
	cd cloud-setup && pyinfra inventory.py deploy.py