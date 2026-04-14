import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

import psycopg2

DB_CONFIG = {"host": "db", "database": "myapp", "user": "dev", "password": "secret"}


def get_user():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL, name VARCHAR);")
    cur.execute("INSERT INTO users (name) VALUES ('Alice') ON CONFLICT DO NOTHING;")
    cur.execute("SELECT name FROM users LIMIT 1;")
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0] if result else "No user"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        user = get_user()
        self.wfile.write(json.dumps({"user": user}).encode())


if __name__ == "__main__":
    print("API server running on port 8000...")
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
