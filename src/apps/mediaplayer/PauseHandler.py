from HttpServlet import HttpServlet
from HttpResponse import HttpResponse
import os


class PauseHandler(HttpServlet):

    def __init__(self, context):
        HttpServlet.__init__(self, context)
        self.context = context
        self.set_static_files_dir(os.path.join(os.path.dirname(__file__), "static/"))

    def service(self, request):
        response = HttpResponse()
        response.set_header("Connection", "close")
        response.set_contents("")

        if "player" in self.context.keys() and self.context["player"] is not None:
            self.context["player"].play_pause()
        return response