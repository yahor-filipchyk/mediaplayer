
from HttpResponse import HttpResponse
from HttpServlet import HttpServlet
import os
import utils


class MainPage(HttpServlet):

    def __init__(self, context):
        HttpServlet.__init__(self, context)
        self.context = context
        self.set_static_files_dir(os.path.join(os.path.dirname(__file__), "static/"))
        self.set_templates_dir(os.path.join(os.path.dirname(__file__), "templates/"))


    def service(self, request):
        response = HttpResponse()
        response.set_header("Connection", "close")
        response.set_contents(utils.load_template("index.html", self.templates_dir))
        now_playing = ""
        if "player" in self.context.keys() and self.context["player"] is not None:
            now_playing = self.context["player"].get_current_file()
            if now_playing is not None and not now_playing == "":
                splitted = now_playing.split("/")
                if splitted is not None and len(splitted) > 0:
                    now_playing = splitted[-1]
            else:
                now_playing = ""
        response.set_attribute("now_playing", now_playing)
        return response