FROM alpine:3.12.1

RUN apk add --no-cache python2 py-pip nmap
COPY ./nmap_exporter.py /
CMD ["python2", "/nmap_exporter.py"]
