from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn


HOST = "localhost"
PORT = 2000

class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()


        self.wfile.write(bytes("<html><body><h1>HEMYO WORLD!</h1><body></html>", "utf-8"))

server = HTTPServer((HOST, PORT), MyServer)
print("Server now running...")
server.serve_forever()
server.server_close()
print("Server stopped!")
