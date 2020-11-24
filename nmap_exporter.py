#!/usr/bin/env python
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import sys
import subprocess
from urlparse import parse_qs, urlparse
import logging
import os


def locate(file):
    # Find the path for fping
    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.exists(os.path.join(path, file)):
            return os.path.join(path, file)
    return "{}".format(file)


def doScan(ip):
    # nmap -sP --host-timeout 1000 --max-retries 100 --dns-servers 192.168.2.3 192.168.2.* -oG n.tmp
    logger.info("START")
    output = []
    #ping_command = '{} -sP --host-timeout 1000 --max-retries 100 --dns-servers 192.168.2.3 {} -oG n.tmp'.format(filepath, ip)
    ping_command = '{} -sP --host-timeout 1 --max-retries 1 --dns-servers 192.168.2.3 {} -oG n.tmp'.format(
        "nmap", ip)

    # Execute and write output to file
    subprocess.Popen(ping_command, stdout=subprocess.PIPE,
                     shell=True).communicate()
    # read file
    cmd_output = str(subprocess.Popen(
        "cat n.tmp", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0])

    # Parse
    for line in cmd_output.split("\n"):
        if "#" not in line:
            if line:
                val = line.replace("\t", " ").split(" ")
                out = "{ip=\"" + val[1] + "\",hostname=\"" + \
                    val[2].replace("(", "").replace(")", "") + "\"}"
                output.append("nmap_scan{} 1".format(out))

    output.append('')
    return output


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


class StartScan(BaseHTTPRequestHandler):
    def do_GET(self):

        message = '\n'.join(doScan('192.168.2.*'))
        # Prepare HTTP status code
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message)
        return


if __name__ == '__main__':
    # Locate the path of fping
    global filepath
    filepath = locate("nmap")
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    port = 9042
    logger.info('Starting server port {}, use <Ctrl-C> to stop'.format(port))
    server = ThreadedHTTPServer(('0.0.0.0', port), StartScan)
    server.serve_forever()
