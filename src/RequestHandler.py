import os
import mimetypes as mime
from HttpResponse import HttpResponse
from HttpRequest import HttpRequest
from HttpServlet import HttpServlet
import request_processors as rp

BUF_SIZE = 4096

class RequestHandler(object):
    
    def __init__(self, addr, socket):
        self.socket = socket
        self.addr = addr

    #noinspection PyUnusedLocal,PyUnusedLocal
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

        request = HttpRequest(request_data)
        processor = rp.get_processor(request)
        if processor is None:
            response = HttpServlet().get_file(request)
        else:
            try:
                # check if static file is requested
                if request.get_header("Referer") is not None:
                    response = processor.get_file(request)
                else :
                    response = processor.service(request)
            except Exception as ex:
                print("An exception inside the app occurred: {0}".format(ex))
                # add different http errors handling. if it will be needed ;)
                request = HttpServlet().service(request)
        self.send_response(response)
        
    def send_response(self, response):
        self.socket.send(response.get_response())
        self.socket.close()