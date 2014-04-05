
from string import Template

HTTP_CODE = "HTTP_CODE"
RESPONSE_STATUS = "RESPONSE_STATUS"
FIRST_ROW = "HTTP/1.1 ${HTTP_CODE} ${RESPONSE_STATUS}"
RETURN = "\r\n"

class http_response(object):
    """An object representation of HTTP response.
    Contains HTTP response headers and HTTP response body.
    Provides full response in form of byte array that can be directly sent to client side.
    """
    
    def __init__(self):
        # default headers
        self.headers = {
            "Content-Type": "text/html; charset=UTF-8",
            "Server": "Simple python server",
        }
        self.contents = []
        self.parameters = {}
        self.attributes = {}
        self.cached_response = None
        self.http_code = 200
        self.response_status = "OK"

    def set_response_code(self, status_code):
        self.http_code = status_code

    def set_response_status(self, status):
        self.response_status = status

    def get_headers(self):
        return self.headers

    def set_header(self, name, value):
        self.headers[name] = value
        self.cached_response = None
        
    def set_contents(self, contents):
        """Contents can represented as string or byte array.
        Content type should be set separately by class user as HTTP response header.
        Content-Length header is set automatically.
        """
        self.contents = contents
        self.cached_response = None
        
    def set_attribute(self, name, value):
        """Passed attributes will be automatically inserted to response body if
        response content is represented as text and has appropriate placeholders.
        """
        self.attributes[name] = value
        self.cached_response = None
        
    def get_response(self):
        """Converts whole response to byte array."""
        if self.cached_response != None:
            return self.cached_response
        # if response body is represented by text replace attributes in text by their values
        if type(self.contents) is str:
            self.apply_attributes()
        self.set_header("Content-Length", len(self.contents))
        response_status = Template(FIRST_ROW).substitute(HTTP_CODE=self.http_code, RESPONSE_STATUS=self.response_status)
        response = bytearray(response_status + RETURN)
        for header_name in self.headers:
            response.extend(header_name + ": " + str(self.headers[header_name]) + RETURN)
        # add return to separate headers from contents
        response.extend(RETURN)
        response.extend(self.contents)
        self.cached_response = response
        return response

    def apply_attributes(self):
        self.contents = Template(self.contents).safe_substitute(self.attributes)