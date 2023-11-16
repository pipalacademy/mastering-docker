

push:
	tar czf mastering-docker.tgz problems/
	scp mastering-docker.tgz anandology.com:tmp/
	cd cloud-setup && pyinfra inventory.py deploy.py