import os
import mimetypes as mime
from http_response import http_response
from http_request import http_request

BUF_SIZE = 4096

STATIC_PATH = os.path.join(os.path.dirname(__file__), "static/")

import request_processors as rp

class ServerThread(object):
    
    def __init__(self, addr, socket):
        self.socket = socket
        self.addr = addr
        
    def process_request(self):
        request_data = ""
        while True:
            data = self.socket.recv(BUF_SIZE)
            if not data:
                self.socket.close()
                return
            request_data += data.decode("utf-8")
            if len(data) < BUF_SIZE:
                break
        request = self.get_request(request_data)
        #print(request)
        processor = self.resolve_request_processor(request)
        response = None
        if processor == None:
            response = self.get_file(request.get_requested_page())
        else:
            response = processor(request)
        self.send_response(response)
        
    def get_file(self, resource):
        response = http_response()
        response.set_header("Connection", "close")
        file_name = os.path.join(os.path.dirname(STATIC_PATH), resource[1:])
        print(file_name)
        mime_type = mime.guess_type(file_name)        
        if (os.path.isfile(file_name)):
            file = open(file_name, "rb")
            file_contents = bytearray(file.read())
            response.set_contents(file_contents)
            response.set_header("Content-Type", mime_type[0])
            file.close()
        else:
            response.set_response_code(404)
            response.set_response_status("Not found")
        return response
        
    def resolve_request_processor(self, request):
        resource = request.get_requested_page()
        if resource != None and resource in rp.processors:
            processor = rp.processors[resource]
            return processor
        else:
            return None
        
    def send_response(self, response):
        response.get_response()
        print(response.get_headers())
        self.socket.send(response.get_response())
        self.socket.close()
        
    def get_request(self, request_plain):
        return http_request(request_plain)