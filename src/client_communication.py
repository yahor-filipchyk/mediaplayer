import os
import mimetypes as mime

BUF_SIZE = 4096
FIRST_ROW_POS = 0
METHOD_POS = 0
RESOURCE_POS = 1
PROTOCOL_POS = 2
HEADER_NAME_POS = 0
HEADER_VALUE_POS = 1
METHOD = "method"
RESOURCE = "resource"
PROTOCOL = "protocol"
HEADERS = "headers"
CONTENTS = "contents"

STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")

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
                break
            request_data += data.decode("utf-8")
            if len(data) < BUF_SIZE:
                break
        request = self.get_request(request_data)
        print(request)
        processor = self.resolve_request_processor(request)
        response = None
        if processor == None:
            response = self.get_file(request[RESOURCE])
        else:
            response = processor(request)
        self.send_response(response)
        
    def get_file(self, resource):
        response = {
        "headers": "HTTP/1.1 200 OK\r\ncontent-type: text/html; charset=UTF-8\r\n\r\n",
        "contents": """
<html>
<head>
    <title>Test page</title>
</head>
<body>
    <h1>Getting a file</h1>
</body>
</html>     
""",
        }
        file_name = os.path.join(STATIC_PATH, resource)
        mime_type = mime.guess_type(file_name)        
        if (os.path.isfile(file_name)):
            file = open(file_name, "r")
            response[CONTENTS] = file.readall()
            file.close()
        else:
            response[CONTENTS] = ""
        print(mime_type)
        return response
        
    def resolve_request_processor(self, request):
        resource = request[RESOURCE]
        if resource != None and resource in rp.processors:
            processor = rp.processors[resource]
            return processor
        else:
            return None
        
    def send_response(self, response):
        self.socket.send(bytearray(response[HEADERS], "utf-8"))
        self.socket.send(bytearray(response[CONTENTS], "utf-8"))
        self.socket.close()
        
    def get_request(self, request_plain):
        request = {}
        parts = request_plain.split("\r\n")
        # splitting first row
        first_row_parts = parts[FIRST_ROW_POS].split()
        request[METHOD] = first_row_parts[METHOD_POS]
        request[RESOURCE] = first_row_parts[RESOURCE_POS]
        request[PROTOCOL] = first_row_parts[PROTOCOL_POS]
        # getting headers
        headers = {}
        for index in range(1, len(parts)):
            header_parts = parts[index].split(": ")
            if len(header_parts) >= 2:
                headers[header_parts[HEADER_NAME_POS]] = header_parts[HEADER_VALUE_POS]
        request[HEADERS] = headers
        return request