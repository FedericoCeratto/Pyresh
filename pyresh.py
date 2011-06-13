#!/usr/bin/env python

"""
pyresh - Python Remote SHell

Cross-platform remote Python interpreter

"""

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from StringIO import StringIO
from string import Template
from time import time
import cgi
import sys

try:
    import ssl
    ssl_available = True
except ImportError:
    ssl_available = False

# Certificate file
PEM = 'cert.pem'

#TODO: specify ports, PEM and ipaddr from CLI
IPADDR = '127.0.0.1'
HTTP_PORT = 8888
HTTPS_PORT = 4433

import BaseHTTPServer, SimpleHTTPServer
import ssl

index = Template("""
    <form name="input" action="/" method="post">
    Code: 
    <textarea name="code" rows="5" cols="60">$code</textarea>
    <input type="hidden" name="format" value="html"/>
    <input type="submit" value="Submit" />
    </form>
""")

class PostHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """
        """
        print "GET received"
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<html><head><title>Pyresh</title></head>")
        self.wfile.write(index.substitute(dict(code='')))
        self.wfile.write("</body></html>")


    def do_POST(self):
        """Execute code
        """
        print "POST received"
        post = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD':'POST',
                'CONTENT_TYPE':self.headers['Content-Type'],
            }
        )
        code = post.getfirst("code","")
        fmt = post.getfirst("format","simple")
        code = code.split('\n')
        code = [s.rstrip() for s in code if s.rstrip()]
        code = '\n'.join(code)

        print "Running:\n---\n%s\n---\n format: %s" % (code, fmt)

        if fmt == "html":
            self.wfile.write("<html><body>%s" % index.substitute(
                dict(code=code)
            ))
        # Intercept stdout/stderr
        stdout = StringIO()
        stderr = StringIO()
        sys.stdout = stdout
        sys.stderr = stderr

        try:
            success = False
            exec code
            stdout = stdout.getvalue()
            stderr = stderr.getvalue()
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            # Succesful response 
            self.send_response(200)
            self.end_headers()
            #TODO: fork and reply to the user while running the code
            
            if fmt == "simple":
                self.wfile.write(stdout)
            elif fmt == "html":
                html = "<h4>Output</h4><pre>" \
                    "%s</pre><h4>Stderr</h4><pre>%s</pre></body></html>" % \
                    (stdout, stderr)
                self.wfile.write(html)
            else:
                raise NotImplementedError
            success = True

        except Exception, e:
        
            stdout = stdout.getvalue()
            stderr = stderr.getvalue()
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            print "Exception: %s" % str(e)
            # Execution failure
            self.send_response(200)
        
            if fmt == "simple":
                self.wfile.write(str(e))
            elif fmt == "html":
                html = "<html><body><h4>Output</h4><pre>" \
                    "%s</pre><pre>%s</pre></body></html>" % \
                    (stdout, str(e))
                self.wfile.write(html)
                print html
            else:
                raise NotImplementedError

        finally:
            # Restores stdout/stderr #TODO: is this really needed?
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

def main():
    
    server_address = ('', 443) # (address, port)

    if ssl_available and True:
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




