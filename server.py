#  coding: utf-8
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


def getFileContents(path):
    fileText = ""
    with open(path, "r") as fin:
        fileText = fin.read()

    return fileText


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        requestParams = self.data.decode().split(' ')
        requestedFile = requestParams[1]
        print("Got a request of: %s\n" % self.data)
        if requestParams[0] == "GET":
            if os.path.exists("./www"+requestedFile):
                self.index("./www"+requestedFile)
            else:
                self.pageNotFound()
        else:
            self.methodNotAllowed()

    def pageNotFound(self):
        self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n", "utf-8"))

    def methodNotAllowed(self):
        self.request.sendall(
            bytearray("HTTP/1.1 405 Method Not Allowed\r\n", "utf-8"))

    def movedPermantently(self, location):
        self.request.sendall(
            bytearray("HTTP/1.1 301 Moved Permanently\r\n", "utf-8"))
        self.request.sendall(
            bytearray("Location:" + self.client_address + location, "utf-8"))

    def serveFile(self, fileText, fileType):
        self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n", "utf-8"))
        self.request.sendall(
            bytearray("Content-Type:" + fileType + "\r\n\n", "utf-8"))
        self.request.sendall(bytearray(fileText, "utf-8"))

    def index(self, path):
        if os.path.isdir(path):
            if path[-1] != "/":
                location = path + "/index.html"
                self.movedPermantently(location)
            path += "index.html"

        fileText = getFileContents(path)
        fileType = "text/html"

        if path[-3:] == "css":
            fileType = "text/css"

        self.serveFile(fileText, fileType)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
