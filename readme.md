# nmap / Device exporter Prometheus

Device scan for Prometheus

![Bild](https://github.com/ToWipf/nmap_exporter/blob/main/grafana.jpg)

## Build and Debug:
```sh
docker run -d --name nmap_exporter -p 9042:80 nmap_exporter

docker build -t nmap_exporter .
docker run -p 9042:80 nmap_exporter
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
