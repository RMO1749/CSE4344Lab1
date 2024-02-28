import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

hostname = "localhost" 
serverPort = 7020


'''Threaded HTTP Server will be responsible for serving multiple requests concurrently/parallel
'''
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

'''
BaseHTTPRequestHandler will be responsible for the initial request of the html being served. 
'''
class MyServer(BaseHTTPRequestHandler):


    
    def do_GET(self):
        # Serve index.html for the root path
        if self.path == "/" or self.path == "/index.html": #when no path is specified we will serve the default html 
            self.serve_html_file("index.html")
        
        elif self.path == '/page1.html':
            self.handle_301_redirect('/page2.html')
        
        elif self.path =="/page2.html":
            self.serve_html_file("page2.html")

        elif self.path.endswith(".jpg") or self.path.endswith(".png"):
            file_path1 = os.path.join(os.getcwd(), self.path.strip("/"))
            self.serve_image_file(file_path1)

        else:
            self.handle_404_not_found()


    def handle_301_redirect(self, new_location):
        self.send_response(301)
        self.send_header("Location", new_location)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        message = (
            "<html><head><title>301 Moved Permanently</title></head><body>"
            "<h1>301 Moved Permanently</h1>"
            f"<p>This page has been permanently moved to <a href='{new_location}'>{new_location}</a>.</p>"
            "</body></html>"
        )
        self.wfile.write(bytes(message, "utf-8"))   


    def serve_html_file(self, file_name):
        try:
            with open(file_name, 'r') as file:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(file.read(), "utf-8"))
        except FileNotFoundError:
            self.handle_404_not_found()
            

    def serve_image_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                self.send_response(200)
                if file_path.endswith(".jpg"):
                    self.send_header("Content-type", "image/jpeg")
                elif file_path.endswith(".png"):
                    self.send_header("Content-type", "image/png")
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.serve_html_file("404.html")

      

    def handle_404_not_found(self):
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.serve_html_file("404.html")


if __name__ == "__main__":
    webServer = ThreadedHTTPServer((hostname, serverPort), MyServer)
    print(f"Server started http://{hostname}:{serverPort}")
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")
