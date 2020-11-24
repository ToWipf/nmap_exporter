# nmap exporter Prometheus

WORK IN PROGRESS! NOT RUNNING NOW

docker build -t nmap_exporter .

docker run -d --name nmap_exporter -p 9042:80 nmap_exporter

docker run -p 9042:80 nmap_exporter
