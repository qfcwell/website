
from http.server import HTTPServer, CGIHTTPRequestHandler
from socketserver import ThreadingMixIn
import ssl

class ThreadingHttpServer( ThreadingMixIn, HTTPServer ):
    pass

port = 4443
#httpd = HTTPServer(('', port), CGIHTTPRequestHandler)
httpd = ThreadingHttpServer(('', port), CGIHTTPRequestHandler)

httpd.socket = ssl.wrap_socket(httpd.socket,
                               server_side=True,
                               certfile='localhost.pem',
                               ssl_version=ssl.PROTOCOL_TLSv1)

     

print("Starting simple_httpd on port: " + str(httpd.server_port))
httpd.serve_forever()


     
