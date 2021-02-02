# nmap / Device scan exporter Prometheus

This Docker Container scans the Target Network on every request. Nmap has a host timeout with 10 sec. and is configured with five retries.

> `docker pull docker.pkg.github.com/towipf/nmap_exporter/nmap_exporter:0.2arm`

![Bild](https://raw.githubusercontent.com/ToWipf/nmap_exporter/main/grafana.png)

## Build and Debug:
```sh
docker build -t nmap_exporter .
docker run -p 9042:80 nmap_exporter

docker run -d --name nmap_exporter -p 9042:80 nmap_exporter
```

## Build Arm:
```sh
docker buildx build --load --platform linux/arm -t nmap_exporter:arm -f arm/Dockerfile .
```

## Config:
```
Todo

Current: hardcoded for 192.168.2.*
```

## Output for Prometheus:
```
nmap_scan{ip="192.168.2.1",hostname="fritz.box"} 1
nmap_scan{ip="192.168.2.42",hostname="device0815"} 1
```
