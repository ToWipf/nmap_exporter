#!/bin/bash
apt install qemu-user
DOCKER_CLI_EXPERIMENTAL=enabled 

docker build . --file Dockerfile --tag docker.pkg.github.com/towipf/nmap_exporter:0.1
docker buildx build --platform linux/arm -t docker.pkg.github.com/towipf/nmap_exporter:0.1arm -f Dockerfile.arm .

docker push docker.pkg.github.com/towipf/nmap_exporter:0.1
docker push docker.pkg.github.com/towipf/nmap_exporter:0.1arm
