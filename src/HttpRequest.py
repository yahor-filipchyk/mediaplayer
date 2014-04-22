
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


class HttpRequest(object):
    """An object representation of HTTP request.
    Gets plain HTTP request, parses it and stores request method,
    requested page, request parameters and headers.
    """

    def __init__(self, request_plain=None):
        self.request = {}
        self.requested_page = None
        self.query_params = {}
        if request_plain is not None:
            self.parse_plain_request(request_plain)

    def parse_plain_request(self, request_plain):
        """Parses plain HTTP request and stores all extracted information"""
        lines = request_plain.split("\r\n")
        # splitting first row
        first_row_parts = lines[FIRST_ROW_POS].split()
        self.request[METHOD] = first_row_parts[METHOD_POS]
        self.request[RESOURCE] = first_row_parts[RESOURCE_POS]

        # getting of requested page
        self.requested_page = self.extract_requested_page(self.request[RESOURCE])

        # extracting of request parameters
        if self.request[METHOD] == "GET":
            self.query_params = self.get_query_params_for_GET(self.request[RESOURCE])
        elif self.request[METHOD] == "POST":
            # TODO: add different request methods handling
            pass

        self.request[PROTOCOL] = first_row_parts[PROTOCOL_POS]
        # getting headers
        headers = {}
        for index in range(1, len(lines)):
            header_parts = lines[index].split(": ")
            if len(header_parts) >= 2:
                headers[header_parts[HEADER_NAME_POS]] = header_parts[HEADER_VALUE_POS]
        self.request[HEADERS] = headers

    def get_requested_resource(self):
        return self.request[RESOURCE]

    @staticmethod
    def extract_requested_page(requested_resource):
        return requested_resource.split("?")[0]

    def get_requested_page(self):
        return self.requested_page

    def get_query_params_for_GET(self, requested_resource):
        """Returns dictionary of request parameters extracted from GET query"""
        string_parts = requested_resource.split("?")
        if len(string_parts) < 2:
            return {}
        query = string_parts[1]
        query_parts = query.split("&")
        for query_part in query_parts:
            params = query_part.split("=")
            if len(params) == 2:
                self.query_params[params[0]] = params[1]
        return self.query_params

    def get_request_params(self):
        return self.query_params

    def get_request_param(self, param_name):
        if param_name in self.query_params.keys():
            return self.query_params[param_name]
        return None

    def get_headers(self):
        return self.request[HEADERS]

    def get_header(self, header_name):
        if header_name in self.request[HEADERS]:
            return self.request[HEADERS][header_name]
        return None

    def get_method(self):
        return self.request[METHOD]

    def get_protocol(self):
        return self.request[PROTOCOL]