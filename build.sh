#!/bin/bash
sudo apt-get install qemu-user -y
DOCKER_CLI_EXPERIMENTAL=enabled 
DOCKER_BUILDKIT=1
BUILDX_NO_DEFAULT_LOAD=arm32v7
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

echo "_______Build_______"
docker build . --file Dockerfile --tag docker.pkg.github.com/towipf/nmap_exporter/nmap_exporter:0.1
echo "_______Build arm_______"
docker buildx build --platform linux/arm -t docker.pkg.github.com/towipf/nmap_exporter/nmap_exporter:0.1arm -f Dockerfile.arm .
echo "_______Push_______"
docker push docker.pkg.github.com/towipf/nmap_exporter/nmap_exporter:0.1
echo "_______Push arm_______"
docker push docker.pkg.github.com/towipf/nmap_exporter/nmap_exporter:0.1arm
