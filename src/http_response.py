
HEADERS = "headers"
CONTENTS = "contents"
FIRST_ROW = "HTTP/1.1 200 OK"
RETURN = "\r\n"
DEFAULT_HEADERS = {
    'Content-Type': "text/html; charset=UTF-8",
}

class http_response(object):
    
    def __init__(self):
        self.headers = DEFAULT_HEADERS
        self.contents = None
        self.parameters = {}
        self.attributes = {}
        self.cached_response = None

    def set_header(self, name, value):
        self.headers[name] = value
        self.cached_response = None
        
    def set_contents(self, contents):
        self.contents = contents
        self.cached_response = None
        
    def set_attribute(self, name, value):
        self.attributes[name] = value
        self.cached_response = None
        
    def get_response(self):
        if self.cached_response != None:
            return self.cached_response
        if type(self.contents) is str:
            self.apply_attributes()
        self.set_header("Content-Length", len(self.contents))
        response = bytearray(FIRST_ROW + RETURN)
        for header_name in self.headers:
            #print(header_name, self.headers[header_name])
            response.extend(header_name + ": " + str(self.headers[header_name]) + RETURN)
        # add return to separate headers from contents
        response.extend(RETURN)
        response.extend(self.contents)
        self.cached_response = response
        return response

    def apply_attributes(self):
        return None