'''
Geo Tracker server


deploy: git push heroku master
url: https://geo-tracker-live.herokuapp.com/


'''
from http.server import BaseHTTPRequestHandler, HTTPServer
from base64 import b64encode, b64decode
import os
import json
import zlib

DEFAULT_PORT = '8080'

class GeoTrackerServer(BaseHTTPRequestHandler):
       def do_GET(self):
              self.send_response(200)
              self.send_header('Content-type', 'application/json')
              self.end_headers()
              
              response = json.dumps([
                     {"lat":21.0, "lng":52.0, "speed": 10, "timestamp": 1569342211},
                     {"lat":21.0, "lng":52.0, "speed": 10, "timestamp": 1569342211},
                     {"lat":21.0, "lng":52.0, "speed": 10, "timestamp": 1569342211},
                     {"lat":21.0, "lng":52.0, "speed": 10, "timestamp": 1569342211},
                     {"lat":21.0, "lng":52.0, "speed": 10, "timestamp": 1569342211},
                     {"lat":21.0, "lng":52.0, "speed": 10, "timestamp": 1569342211}
              ])
              
              #compressed = b64encode(
              #       zlib.compress(
              #              response.encode("utf-8")
              #       )
              #).decode("ascii")
              
              self.wfile.write(response.encode())

def run(server_class=HTTPServer, handler_class=GeoTrackerServer, port=DEFAULT_PORT):
       server_address = ('', int(port))
       httpd = server_class(server_address, handler_class)
       try:
              httpd.serve_forever()
       except KeyboardInterrupt:
              pass
       httpd.server_close()
 
if __name__ == '__main__':
       run(port = os.environ['PORT'] if 'PORT' in os.environ else DEFAULT_PORT)
