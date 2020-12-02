#!/usr/bin/env python
from http.server import BaseHTTPRequestHandler, HTTPServer
from subprocess import check_output

def doScan(ip, dns):
    output = []
    ping_command = '/usr/bin/nmap -sP --host-timeout 10 --max-retries 5 --dns-servers {} {} -oG n.tmp'.format(dns, ip)

    # Execute and write output to file
    try:
        check_output(ping_command, shell=True, timeout=5)
    except Exception:
        pass
        fout = "{ip=\"" + "scan_failed" + "\",hostname=\"" + "scan_failed"+ "\"}"
        output.append("nmap_scan{} 1".format(fout))
        return output

    with open("n.tmp") as f:
        cmd_output = f.readlines()

    # Parse
    for line in cmd_output:
        if "#" not in line:
            if line:
                val = line.replace("\t", " ").split(" ")
                out = "{ip=\"" + val[1] + "\",hostname=\"" + val[2].replace("(", "").replace(")", "") + "\"}"
                output.append("nmap_scan{} 1".format(out))

    output.append('')
    return output


class StartScan(BaseHTTPRequestHandler):
    def do_GET(self):
        message = '\n'.join(doScan('192.168.2.*', '192.168.2.3'))

        self.send_response(200)
        self.end_headers()
        self.wfile.write(message.encode())
        return

if __name__ == '__main__':
    port = 80
    httpdserver = HTTPServer(('0.0.0.0', port), StartScan)
    try:
        httpdserver.serve_forever()
    except KeyboardInterrupt:
        pass
        httpdserver.server_close()
