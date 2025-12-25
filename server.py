from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from datetime import datetime
import json

load_dotenv()
PORT = int(os.getenv('PORT'));

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()
        
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path     
        
        if path == '/get-data-presence':
          try:
            today = datetime.today().strftime('%Y-%m-%d')
            filename = f'absensi-{today}.md'   
            
            with open(filename, encoding="utf-8") as f:
              content = f.read();
                
            data = json.loads(content)
                
            response_body = json.dumps(data).encode("utf-8")
      
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Content-Length", str(len(response_body)))
            self.end_headers()
            
            self.wfile.write(response_body)
            
          except FileNotFoundError:
            self.send_error(404, "File not found")
          except json.JSONDecodeError:
            self.send_error(500, "Invalid JSON format")
        else:
          self.send_error(404, "Not Found")
          return
            
        f.close()

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print("serving at port", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Stopping server.")

if __name__ == "__main__":
    run()