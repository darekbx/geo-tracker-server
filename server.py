'''
Geo Tracker server
 - /location-data?limit=100 [GET], download latest location data
 - /save-location [POST], save single location data

 Location data model:
 { 
        "lat": 21.000000           # floating point with 6 decimal places
        "lng": 52.000000           # floating point with 6 decimal places
        "speed": 23.5              # km\h
        "timestamp": 1569342211    # timestamp of the sample
        "track_id": 12             # identifier of the track
 }

TODO:
 - authentication (provide a token?)
 - postgres db: https://devcenter.heroku.com/articles/getting-started-with-python#provision-a-database

'''
from http.server import BaseHTTPRequestHandler, HTTPServer
from base64 import b64encode, b64decode
from urllib.parse import urlparse, parse_qs
import os
import json
import zlib

DEFAULT_PORT = '8080'

class GeoTrackerServer(BaseHTTPRequestHandler):

       LOCATION_DATA_PATH = "/location-data"
       SAVE_LOCATION_PATH = "/save-location"

       def do_GET(self):
              url = urlparse(self.path)
              if url.path != self.LOCATION_DATA_PATH:
                     self._end_with_404()
                     self.wfile.write("HTTP 404".encode())
                     return

              if self.headers['Authorization'] != "Basic {0}".format(os.environ["BASIC_TOKEN"]):
                     self._end_with_401()
                     self.wfile.write("HTTP 401".encode())
                     return
              
              query = parse_qs(url.query)
              limit = query['limit'][0]

              response = json.dumps([
                     {"lat":21.0, "lng":52.0, "speed": 10, "timestamp": 1569342211, "track_id": 12},
                     {"lat":21.0, "lng":52.0, "speed": 10, "timestamp": 1569342211, "track_id": 12},
                     {"lat":21.0, "lng":52.0, "speed": 10, "timestamp": 1569342211, "track_id": 12},
                     {"lat":21.0, "lng":52.0, "speed": 10, "timestamp": 1569342211, "track_id": 12},
                     {"lat":21.0, "lng":52.0, "speed": 10, "timestamp": 1569342211, "track_id": 12},
                     {"lat":21.0, "lng":52.0, "speed": 10, "timestamp": 1569342211, "track_id": 12}
              ])
              
              #compressed = b64encode(
              #       zlib.compress(
              #              response.encode("utf-8")
              #       )
              #).decode("ascii")
              
              self.send_response(200)
              self.send_header('Content-type', 'application/json')
              self.end_headers()
              self.wfile.write(response.encode())

       def do_POST(self):
              if self.path != self.SAVE_LOCATION_PATH:
                     self._end_with_404()
                     return
              pass

       def _end_with_404(self):
              self.send_response(404)
              self.end_headers()

       def _end_with_401(self):
              self.send_response(401)
              self.end_headers()


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
