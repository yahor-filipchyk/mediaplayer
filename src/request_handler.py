import os
import mimetypes as mime
from http_response import http_response
from http_request import http_request
import request_processors as rp

BUF_SIZE = 4096

STATIC_PATH = os.path.join(os.path.dirname(__file__), "static/")

class request_handler(object):
    
    def __init__(self, addr, socket):
        self.socket = socket
        self.addr = addr
        
    def process_request(self):
        request_data = ""
        while True:
            data = self.socket.recv(BUF_SIZE)
            if not data:
                if request_data == "":
                    self.socket.close()
                    return
                break
            request_data += data.decode("utf-8")
            if len(data) < BUF_SIZE:
                break
        request = http_request(request_data)
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
        file_name = os.path.join(os.path.dirname(STATIC_PATH), resource[1:] if resource.startswith("/") else resource)
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
        return rp.get_processor(request.get_requested_page())
        
    def send_response(self, response):
        self.socket.send(response.get_response())
        self.socket.close()