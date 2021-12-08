from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json


hostName = "localhost"
serverPort = 8080
class MyServer(BaseHTTPRequestHandler):
    def do_POST(self):
        length = self.headers["Content-Length"]
        body = (self.rfile.read(int(length)).decode('utf-8'))[1:-1]
        body = body.replace('\"', '')
        urls = body.split(",")
        nums = [1.0, 0.56, 0.43, -0.78]
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(nums), "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
