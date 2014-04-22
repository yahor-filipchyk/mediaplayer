from HttpServlet import HttpServlet
from HttpResponse import HttpResponse
import os
import urllib.parse as urlparse
from apps.mediaplayer.OSMediaPlayer import OSMediaPlayer
from apps.mediaplayer.MediaPlayer import MUSIC_FILES_DIR
from apps.mediaplayer.MediaPlayer import VIDEO_FILES_DIR
from apps.mediaplayer.MPlayer import MPlayer


class PlayHandler(HttpServlet):

    def __init__(self, context):
        HttpServlet.__init__(self, context)
        self.context = context
        self.set_static_files_dir(os.path.join(os.path.dirname(__file__), "static/"))

    def service(self, request):
        response = HttpResponse()
        response.set_header("Connection", "close")
        response.set_contents("")
        print("PAGE: " + request.get_requested_page())
        MEDIA_DIR = MUSIC_FILES_DIR if request.get_requested_page().startswith("/music") else VIDEO_FILES_DIR
        subdir = request.get_request_param("folder")
        to_play = None
        if subdir is not None:
            subdir = urlparse.unquote(subdir, "utf-8")
            music_dir = os.path.join(MEDIA_DIR, subdir)
            print("PLAYING DIR: " + music_dir)
            to_play = music_dir
        elif request.get_request_param("file") is not None:
            music_file = request.get_request_param("file")
            if music_file is not None:
                music_file = urlparse.unquote(music_file, "utf-8")
                print("PLAYING FILE: " + music_file)
                to_play = os.path.join(MEDIA_DIR, music_file)
        elif request.get_request_param("switch") is not None:
            where = request.get_request_param("switch")
            if "player" in self.context.keys() and self.context["player"] is not None:
                if where == "previous":
                    self.context["player"].previous()
                elif where == "next":
                    self.context["player"].next()

        if to_play is not None and not "player" in self.context.keys() or self.context["player"] is None:
            self.context["player"] = MPlayer()
            print("new player was created")
        if to_play is not None:
            if MEDIA_DIR == VIDEO_FILES_DIR:
                self.context["player"].play(to_play, OSMediaPlayer.TYPE_VIDEO)
            else:
                self.context["player"].play(to_play)
        return response