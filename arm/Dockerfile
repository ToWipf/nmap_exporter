FROM arm32v7/alpine:3.12.1

RUN apk add --no-cache python3 py-pip nmap
COPY ./nmap_exporter.py /
CMD ["python3", "/nmap_exporter.py"]
