#!/usr/bin/env python

"""
pyresh - Python Remote SHell

Cross-platform remote Python interpreter

"""

from SocketServer import BaseServer
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SimpleHTTPServer import SimpleHTTPRequestHandler
from OpenSSL import SSL
import cgi
from sys import exit

# Certificate file
PEM = './cert.pem'

#TODO: specify ports, and ipaddr from CLI
HTTP_PORT = 8888
HTTPS_PORT = 4433

class HTTPSserver(HTTPServer):
    def __init__(self, server_address, HandlerClass):
        BaseServer.__init__(self, server_address, HandlerClass)
        try:
            ctx = SSL.Context(SSL.SSLv23_METHOD)
            ctx.use_privatekey_file (PEM)
            ctx.use_certificate_file(fpem)
            self.socket = SSL.Connection(ctx, socket.socket(self.address_family,
                                                        self.socket_type))
            self.server_bind()
            self.server_activate()
        except Exception, e:
            print e
            exit(1)

class HTTPSRequestHandler(SimpleHTTPRequestHandler):
    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)


def test(HandlerClass = SecureHTTPRequestHandler,
         ServerClass = SecureHTTPServer):
    server_address = ('', 443) # (address, port)
    httpd = ServerClass(server_address, HandlerClass)
    sa = httpd.socket.getsockname()
    print "Serving HTTPS on", sa[0], "port", sa[1], "..."
    httpd.serve_forever()



class PostHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        try:
            # Succesful response 
            self.send_response(200)
            self.end_headers()
            self.wfile.write('Client: %s\n' % str(self.client_address))
        
        except Exception, e:
            # Execution failurie
            self.send_response(400)


def main():
    server = HTTPServer(('', HTTP_PORT), PostHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()




