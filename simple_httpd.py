
from http.server import HTTPServer, CGIHTTPRequestHandler
from socketserver import ThreadingMixIn

class ThreadingHttpServer( ThreadingMixIn, HTTPServer ):
    pass

port = 8080
#httpd = HTTPServer(('', port), CGIHTTPRequestHandler)
httpd = ThreadingHttpServer(('', port), CGIHTTPRequestHandler)



     

print("Starting simple_httpd on port: " + str(httpd.server_port))
httpd.serve_forever()


     
