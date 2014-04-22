
from HttpResponse import HttpResponse
from HttpServlet import HttpServlet
import os
import utils


class MainServlet(HttpServlet):

    def __init__(self, context):
        HttpServlet.__init__(self, context)
        self.set_static_files_dir(os.path.join(os.path.dirname(__file__), "static/"))

    def service(self, request):
        response = HttpResponse()
        response.set_header("Connection", "close")
        response.set_contents(utils.load_template("index.html", self.templates_dir))
        response.set_attribute("title", "Home python server")
        return response