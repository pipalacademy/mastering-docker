
build:
	quarto render

preview:
	quarto preview --port 5050

deploy: build
	rsync -av _site/* docker.pipal.in:/var/www/docker.pipal.in/


