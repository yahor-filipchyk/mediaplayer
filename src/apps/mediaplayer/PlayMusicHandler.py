from HttpServlet import HttpServlet
from HttpResponse import HttpResponse
import os
import urllib.parse as urlparse
from apps.mediaplayer.MusicPlayer import MUSIC_FILES_DIR


class PlayMusicHandler(HttpServlet):

    def __init__(self, context):
        HttpServlet.__init__(self, context)
        self.set_static_files_dir(os.path.join(os.path.dirname(__file__), "static/"))

    def service(self, request):
        response = HttpResponse()
        response.set_header("Connection", "close")
        response.set_contents("")
        subdir = request.get_request_param("folder")
        if subdir is not None:
            subdir = urlparse.unquote(subdir, "utf-8")
            music_dir = os.path.join(MUSIC_FILES_DIR, subdir)
            print("PLAYING DIR: " + music_dir)
        else:
            music_file = request.get_request_param("file")
            if music_file is not None:
                music_file = urlparse.unquote(music_file, "utf-8")
                print("PLAYING FILE: " + music_file)
        return response