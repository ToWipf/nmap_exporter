#!/usr/bin/env python
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import subprocess


def doScan(ip):
    output = []
    ping_command = '{} -sP --host-timeout 10 --max-retries 5 --dns-servers 192.168.2.3 {} -oG n.tmp'.format(
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
    port = 80
    print('Starting toWipf device scanner Version 0.1 on port {}'.format(port))
    server = ThreadedHTTPServer(('0.0.0.0', port), StartScan)
    server.serve_forever()
