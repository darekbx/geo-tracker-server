'''
Geo Tracker server
 - /location-data?limit=100 [GET], download latest location data
 - /save-location [POST], save single location data

 Location data model:
 { 
    "lat": 21.000000           # floating point with 6 decimal places
    "lng": 52.000000           # floating point with 6 decimal places
    "speed": 23.5              # speed in km\h
    "timestamp": 1569342211    # timestamp of the sample
    "track_id": 12             # identifier of the track
 }
'''
import os
import json
import psycopg2
from psycopg2 import Error
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class GeoTrackerDB:

    connection = None
    cursor = None

    def connect(self):
        try:
            if 'DATABASE_URL' in os.environ:
                db_url = psycopg2.connect(os.environ['DATABASE_URL'])
            else:
                db_url = "" # Take from heroku variables 
            self.connection = psycopg2.connect(db_url)
            self.cursor = self.connection.cursor()
            self.init_scheme()
        except (Exception, Error) as error:
                print("Error while connecting to PostgreSQL", error)
        
    def init_scheme(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS positions (
                id integer generated always as identity,
                lat real NOT NULL,
                lng real NOT NULL,
                speed real NOT NULL,
                timestamp bigint NOT NULL,
                track_id integer NOT NULL,
                PRIMARY KEY (id)
            )                    
        ''')
        self.connection.commit()

    def fetch_all(self, limit):
        self.cursor.execute("SELECT * FROM positions LIMIT {0}".format(limit))
        return self.cursor.fetchall()

    def add(self, data):
        self.cursor.execute("INSERT INTO positions (lat, lng, speed, timestamp, track_id) VALUES(%s, %s, %s, %s, %s)", data)
        self.connection.commit()

    def close(self):
        if (self.connection):
            self.cursor.close()
            self.connection.close()

class GeoTrackerServer(BaseHTTPRequestHandler):

    LOCATION_DATA_PATH = "/location-data"
    SAVE_LOCATION_PATH = "/save-location"

    db = GeoTrackerDB()

    def do_GET(self):
        url = urlparse(self.path)
        
        if url.path != self.LOCATION_DATA_PATH:
            self._end_with_404()
            return

        if self._is_authorized():
            self._end_with_401()
            return

        query = parse_qs(url.query)
        limit = query['limit'][0]

        self.db.connect()
        rows = self.db.fetch_all(limit)
        self.db.close()

        named_rows = []
        for row in rows:
            named_rows.append({ "lat": row[1], "lng": row[2], "speed": row[3], "timestamp": row[4], "track_id": row[5] })
        response = json.dumps(named_rows)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response.encode())

    def do_POST(self):
        url = urlparse(self.path)

        if url.path != self.SAVE_LOCATION_PATH:
            self._end_with_404()
            return

        if self._is_authorized():
            self._end_with_401()
            return
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        query = parse_qs(post_data.decode())

        data = (
            query["lat"][0], 
            query["lng"][0], 
            query["speed"][0], 
            query["timestamp"][0], 
            query["track_id"][0], 
        )

        self.db.connect()
        self.db.add(data)
        self.db.close()

        self.send_response(201)
        self.end_headers()

    def _is_authorized(self):
        basic_token = ""
        if 'BASIC_TOKEN' not in os.environ:
            basic_token = "token"
        else:
            basic_token = os.environ["BASIC_TOKEN"]
        return self.headers['Authorization'] != "Basic {0}".format(basic_token)

    def _end_with_404(self):
        self.send_response(404)
        self.end_headers()

    def _end_with_401(self):
        self.send_response(401)
        self.end_headers()

def run(server_class=HTTPServer, handler_class=GeoTrackerServer, port = ""):
    server_address = ('', int(port))
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    DEFAULT_PORT = '8080'
    run(port = os.environ['PORT'] if 'PORT' in os.environ else DEFAULT_PORT)
