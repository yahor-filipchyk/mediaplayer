from HttpServlet import HttpServlet
from HttpResponse import HttpResponse
import os


class NowPlaying(HttpServlet):

    def __init__(self, context):
        HttpServlet.__init__(self, context)
        self.context = context
        self.set_static_files_dir(os.path.join(os.path.dirname(__file__), "static/"))

    def service(self, request):
        response = HttpResponse()
        response.set_header("Connection", "close")
        response.set_header("Content-Type", "application/xml")
        response.set_contents("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
                              "<playing>${playing}</playing>")
        now_playing = ""
        if "player" in self.context.keys() and self.context["player"] is not None:
            now_playing = self.context["player"].get_current_file()
            if now_playing is not None and not now_playing == "":
                splitted = now_playing.split("/")
                if splitted is not None and len(splitted) > 0:
                    now_playing = splitted[-1]
            else:
                now_playing = ""
        response.set_attribute("playing", now_playing)
        # print(now_playing)
        return response