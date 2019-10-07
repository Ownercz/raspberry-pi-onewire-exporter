from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import os
from pathlib import Path
# Author: Ownercz 
# Contact: radim@lipovcan.cz
# Tested with SZN RPI 3B running Raspbian Stretch
# Crontab entry:
# @reboot /usr/bin/screen -dmS exporter /usr/bin/python3 "/home/pi/exporter.py"

def gettemp():
        temps = {}
        html = []
        absolutePathForSZNPI = '/sys/bus/w1/devices/28-0312979401d5/w1_slave'
        name, path = os.path.split(absolutePathForSZNPI)

        f = open(absolutePathForSZNPI, "r")
        line = f.readlines()
        check = re.findall("([\S\s]=.* +)(.*)",line[0])
        parsedTemp = re.findall("([\S\s]=+)(.*)",line[1])
        f.close

        regexed = re.findall("[^\/]+$",name)
        temps[regexed[0]] = (int(parsedTemp[0][1])/1000)

        #Generate html for exporter
        for temp in temps:
            if check[0][1] == "YES": html.append(str(temps[temp]))
        return html

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
  def handle(self):
      try:
          BaseHTTPRequestHandler.handle(self)
      except socket.error as err:
          pass
  # GET
  def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/plain')
        self.end_headers()

        # Send message back to client
        message = '\n'.join(map(str, gettemp()))
        #message = gettemp()
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

def run():
  print('starting server...')

  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('0.0.0.0', 8082)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()


run()
