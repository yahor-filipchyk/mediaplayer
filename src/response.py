
HEADERS = "headers"
CONTENTS = "contents"
FIRST_ROW = "first_row"
DEFAULT_HEADERS = {
    FIRST_ROW: "HTTP/1.1 200 OK\r\n",
    'content-type': "text/html; charset=UTF-8\r\n",
}

class response(object):
    
    def __init__(self):
        self.headers = {
              HEADERS: DEFAULT_HEADERS,
              CONTENTS: "",      
        }
        self.contents = None
        self.parameters = {}
        self.attributes = {}

    def add_header(self, name, value):
        self.headers[name] = value
        
    def set_contents(self, contents):
        self.contents = contents
        
    def add_attribute(self, name, value):
        self.attributes[name] = value
        
    def get_response(self):
        pass