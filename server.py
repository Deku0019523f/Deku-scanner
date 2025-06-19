from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
from urllib.parse import urlparse, parse_qs

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/scan"):
            mode = parse_qs(urlparse(self.path).query).get("mode", [""])[0]
            if mode == "root":
                result = subprocess.getoutput("./scan_root.sh")
            else:
                result = subprocess.getoutput("./scan_noroot.sh")
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(result.encode())
        else:
            try:
                with open("index.html", "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content)
            except:
                self.send_error(404)

print("🚀 Serveur sur http://localhost:8000")
HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
