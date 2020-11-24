#FROM alpine:3.6
FROM debian:9

#RUN apk add --no-cache nginx-mod-http-lua nmap
RUN apt-get update && apt-get install libnginx-mod-http-lua nmap -y

# Delete default config
RUN rm -r /etc/nginx/conf.d && rm /etc/nginx/nginx.conf

# Create folder for PID file
RUN mkdir -p /run/nginx

# Add our nginx conf
COPY nginx.conf /etc/nginx/nginx.conf

COPY scan.sh /scan.sh
COPY scan.conf /etc/nginx/conf.d/scan.conf

RUN chmod +x /scan.sh

CMD ["nginx"]