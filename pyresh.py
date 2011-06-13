#!/usr/bin/env python

"""
pyresh - Python Remote SHell

Cross-platform remote Python interpreter

"""

from SocketServer import BaseServer
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SimpleHTTPServer import SimpleHTTPRequestHandler
from StringIO import StringIO
import cgi
import sys

try:
    import ssl
    ssl_available = True
except ImportError:
    ssl_available = False

# Certificate file
PEM = './cert.pem'

#TODO: specify ports, PEM and ipaddr from CLI
IPADDR = '127.0.0.1'
HTTP_PORT = 8888
HTTPS_PORT = 4433

import BaseHTTPServer, SimpleHTTPServer
import ssl

class PostHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """
        """
        print "GET"
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<html><head><title>Pyresh</title></head>")
        self.wfile.write("""
        <form name="input" action="/" method="post">
        Code: <input type="text" name="code" />
        <input type="submit" value="Submit" />
        </form>""")
        self.wfile.write("</body></html>")


    def do_POST(self):
        """Execute code
        """
        post = cgi.FieldStorage()
        code = post.getfirst("code","")
        print "Running: '%s'" % code
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
            else:
                raise NotImplementedError
        
        except Exception, e:
            # Execution failurie
            self.send_response(400)
        
        finally:
            # Restores stdout/stderr #TODO: is this really needed?
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

def main():
    
    server_address = ('', 443) # (address, port)

    if ssl_available and False:
        server = HTTPServer((IPADDR, HTTPS_PORT), PostHandler)
        server.socket = ssl.wrap_socket(server.socket,
            certfile=PEM, server_side=True)
    else:
        server = HTTPServer((IPADDR, HTTP_PORT), PostHandler)
    
    sa = server.socket.getsockname()
    print "Serving HTTPS on", sa[0], "port", sa[1], "..."
    server.serve_forever()

if __name__ == '__main__':
    main()




