from http_response import http_response


def get_index(request):
    response = http_response()
    response.set_header("Connection", "close")
    response.set_contents("""
<html>
<head>
    <title>Test page</title>
</head>
<body>
    <h1>Request is processed</h1>
</body>
</html>     
""")
    return response

# predefined request processors
# TODO: add dynamic processors finding
processors = {
    "/": get_index,
}