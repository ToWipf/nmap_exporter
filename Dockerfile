FROM alpine:3.12.1

RUN apk add --no-cache python3 py-pip nmap
COPY ./nmap_exporter.py /
COPY ./start.sh /
CMD "/start.sh"