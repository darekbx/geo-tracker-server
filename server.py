from http.server import BaseHTTPRequestHandler, HTTPServer
import os

DEFAULT_PORT = 8080

class GeoTrackerServer(BaseHTTPRequestHandler):
       def do_GET(self):
              self.send_response(200)
              self.send_header('Content-type', 'text/html')
              self.end_headers()
              self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=GeoTrackerServer, port = DEFAULT_PORT):
       server_address = ('', port)
       httpd = server_class(server_address, handler_class)
       try:
              httpd.serve_forever()
       except KeyboardInterrupt:
              pass
       httpd.server_close()
 
if __name__ == '__main__':
       run(port = os.environ['PORT'] if 'PORT' in os.environ else DEFAULT_PORT)
