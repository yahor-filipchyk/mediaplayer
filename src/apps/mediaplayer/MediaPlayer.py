from HttpServlet import HttpServlet
from HttpResponse import HttpResponse
import os
import utils
import re
import urllib.parse as urlparse

MUSIC_FILES_DIR = "/media/yahor/STORAGE/Music"
VIDEO_FILES_DIR = "/media/yahor/STORAGE/Video"


class MediaPlayer(HttpServlet):

    def __init__(self, context):
        HttpServlet.__init__(self, context)
        self.context = context
        self.set_static_files_dir(os.path.join(os.path.dirname(__file__), "static/"))
        self.set_templates_dir(os.path.join(os.path.dirname(__file__), "templates/"))

    def service(self, request):
        response = HttpResponse()
        response.set_contents(utils.load_template("media.html", self.templates_dir))
        MEDIA_DIR = MUSIC_FILES_DIR if request.get_requested_page().startswith("/music") else VIDEO_FILES_DIR
        media_type = "music" if MEDIA_DIR == MUSIC_FILES_DIR else "video"
        search_pattern = "^.*\.(mp3|wma|wav|)$" if media_type == "music" else "^.*\.(avi|flv|wmv|)$"
        file_names = {"dirs": [], "files": []}
        # getting requested sub-folder
        subdir = request.get_request_param("folder")
        if subdir is not None:
            subdir = urlparse.unquote(subdir, "utf-8")
            media_dir = os.path.join(MEDIA_DIR, subdir)
        else:
            media_dir = MEDIA_DIR
            subdir = ""
        # listing files, names of that will be sent to client
        files = []
        try:
            files = os.listdir(media_dir)
        except FileNotFoundError as err:
            print("Directory wasn't found")
        for file in files:
            if re.match(search_pattern, file):
                file_names["files"].append([subdir, file])
            elif os.path.isdir(os.path.join(media_dir, file)):
                file_names["dirs"].append([subdir, file])
        files_list = ""
        if media_dir != MEDIA_DIR and media_dir[:-1] != MEDIA_DIR:
            parent_folder = os.path.dirname(media_dir)
            # print("PARENT: " + parent_folder)
            if parent_folder != MEDIA_DIR:
                link = "{1}?folder={0}".format(parent_folder.rsplit("/", 1)[1], media_type)
            else:
                link = media_type
            files_list += "<div><a href=\"{0}\"><span class=\"folder\">{1}</span></a></div>\r\n"\
                .format(link, "...")
        for folder in sorted(file_names["dirs"]):
            files_list += "<div><a href=\"{2}?folder={0}\"><span class=\"folder\">{1}</span></a>" \
                          "<span class=\"play-btn\" onclick=\"playFolder('{2}', '{0}')\">" \
                          "Play</span></div>\r\n"\
                .format(os.path.join(folder[0], folder[1]), folder[1], media_type)
        for file in sorted(file_names["files"]):
            files_list += "<div onclick=\"playTrack('{2}', '{1}')\">{0}</div>\r\n".format(file[1],
                        re.sub("'", "\\'", os.path.join(file[0], file[1])), media_type)
        response.set_attribute("files", files_list)
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
        title = "Video" if media_type == "video" else "Music"
        title += "" if subdir == "" else ": " + subdir
        response.set_attribute("title", title)
        return response