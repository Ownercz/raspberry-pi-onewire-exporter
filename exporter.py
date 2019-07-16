from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import os
from pathlib import Path
# Author: Ownercz 
# Contact: radim@lipovcan.cz
# Tested with RPI 2B+ running Raspbian Buster
# Crontab entry:
# @reboot /usr/bin/screen -dmS exporter /usr/bin/python3 "/home/pi/exporter.py"
def gettemp():
        temps = {}
        html = []
        for filename in Path('/sys/bus/w1/devices/').glob('*/w1_slave'):
            name, path = os.path.split(filename)
#            print(filename)
#            print(name)

            f = open(filename, "r")
            line = f.readlines()
#            print(line[1])

            check = re.findall("([\S\s]=.* +)(.*)",line[0])
            parsedTemp = re.findall("([\S\s]=+)(.*)",line[1])
#            print(check)
#            print(parsedTemp)
            f.close

            regexed = re.findall("[^\/]+$",name)
#            print(regexed)
            temps[regexed[0]] = (int(parsedTemp[0][1])/1000)
#            print(temps)
        html.append("# HELP onewire A summary of the GC invocation durations.")
        html.append("# TYPE onewire gauge")
        for temp in temps:
            if check[0][1] == "YES": html.append('onewire_sensor{id="' + str(temp) + '"} ' + str(temps[temp]))
            
#        print(html)
        return html
# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
 
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
  server_address = ('0.0.0.0', 8081)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()
 
 
run()

