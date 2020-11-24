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
    ping_command = '{} -sP --host-timeout 1000 --max-retries 100 --dns-servers 192.168.2.3 {}'.format(filepath, ip)

    output = []

    logger.info("START")

    # Execute
    cmd_output = subprocess.Popen(ping_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()

    # # Parse
    # try:
    #     loss = cmd_output[1].split("%")[1].split("/")[2]
    #     min = cmd_output[1].split("=")[2].split("/")[0]
    #     avg = cmd_output[1].split("=")[2].split("/")[1]
    #     max = cmd_output[1].split("=")[2].split("/")[2].split("\n")[0]
    # except IndexError:
    #     loss = 100
    #     min = 0
    #     avg = 0
    #     max = 0

    # # Gen metrics
    # output.append("ping_avg {}".format(avg))
    # output.append("ping_max {}".format(max))
    # output.append("ping_min {}".format(min))
    # output.append("ping_loss {}".format(loss))
    # output.append('')
    # return output
    return cmd_output


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
