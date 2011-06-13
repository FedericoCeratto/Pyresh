#!/usr/bin/env python

"""
pyresh - Python Remote SHell

Cross-platform remote Python interpreter

"""

from SocketServer import BaseServer
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SimpleHTTPServer import SimpleHTTPRequestHandler
from StringIO import StringIO
from OpenSSL import SSL
import cgi
import sys

# Certificate file
PEM = './cert.pem'

#TODO: specify ports, PEM and ipaddr from CLI
IPADDR = ''
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
        """Execute code
        """
        post = cgi.FieldStorage()
        code = post.getfirst("code","")
        fmt = post.getfirst("format","simple")

        # Intercept stdout/stderr
        stdout = StringIO()
        stderr = StringIO()
        sys.stdout = stdout
        sys.stderr = stderr

        try:
            exec code
            # Succesful response 
            self.send_response(200)
            self.end_headers()
            
            #TODO: fork and reply to the user while running the code
            
            if fmt == "simple":
                self.wfile.write(stdout.getvalue())
            elif fmt == "html":
                html = "<html><body><h4>Output</h4><pre>" \
                    "%s</pre><pre>%s</pre></body></html>" % \
                    (stout.getvalue(),stderr.getvalue())
        
        except Exception, e:
            # Execution failurie
            self.send_response(400)
        
        finally:
            # Restores stdout/stderr #TODO: is this really needed?
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

def main():
    server = HTTPServer(('', HTTP_PORT), PostHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()




