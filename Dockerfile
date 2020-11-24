FROM alpine:latest

RUN apk update && apk add python2 py-pip nmap
COPY ./nmap_exporter.py /
EXPOSE 8085
CMD ["python2", "/nmap_exporter.py"]
