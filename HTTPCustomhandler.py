import http.server
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Send response status code
        self.send_response(200)
        
        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Send the response message
        self.wfile.write(b"Hello, this is a response to your GET request!")
        
        # Close the server after serving one request
        print("Served one GET request, shutting down the server.")
        self.server.shutdown()