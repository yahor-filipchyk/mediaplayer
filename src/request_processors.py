

def get_index(request):
    response = {
        "headers": "HTTP/1.1 200 OK\r\ncontent-type: text/html; charset=UTF-8\r\n\r\n",
        "contents": """
<html>
<head>
    <title>Test page</title>
</head>
<body>
    <h1>Request is processed</h1>
</body>
</html>     
""",
    }
    return response

processors = {
    "/": get_index,
}