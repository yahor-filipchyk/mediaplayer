from HttpServlet import HttpServlet
from HttpResponse import HttpResponse
import os
import utils
import re
import urllib.parse as urlparse

MUSIC_FILES_DIR = "/media/yahor/STORAGE/Music/Music"


class MusicPlayer(HttpServlet):

    def __init__(self, context):
        HttpServlet.__init__(self, context)
        self.set_static_files_dir(os.path.join(os.path.dirname(__file__), "static/"))
        self.set_templates_dir(os.path.join(os.path.dirname(__file__), "templates/"))

    def service(self, request):
        response = HttpResponse()
        response.set_contents(utils.load_template("index.html", self.templates_dir))
        file_names = {"dirs": [], "files": []}
        # getting requested sub-folder
        subdir = request.get_request_param("folder")
        if subdir is not None:
            subdir = urlparse.unquote(subdir, "utf-8")
            music_dir = os.path.join(MUSIC_FILES_DIR, subdir)
        else:
            music_dir = MUSIC_FILES_DIR
            subdir = ""
        # listing files, names of that will be sent to client
        files = []
        try:
            files = os.listdir(music_dir)
        except FileNotFoundError as err:
            print("Directory wasn't found")
        for file in files:
            if re.match("^.*\.(mp3|wma|wav)$", file):
                file_names["files"].append([subdir, file])
            elif os.path.isdir(os.path.join(music_dir, file)):
                file_names["dirs"].append([subdir, file])
        files_list = ""
        if music_dir != MUSIC_FILES_DIR and music_dir[:-1] != MUSIC_FILES_DIR:
            parent_folder = os.path.dirname(music_dir)
            print("PARENT: " + parent_folder)
            if parent_folder != MUSIC_FILES_DIR:
                link = "music?folder={0}".format(parent_folder.rsplit("/", 1)[1])
            else:
                link = "music"
            files_list += "<div><a href=\"{0}\">{1}</a></div>\r\n"\
                .format(link, "...")
        for folder in sorted(file_names["dirs"]):
            files_list += "<div><a href=\"music?folder={0}\">{1}</a></div>\r\n"\
                .format(os.path.join(folder[0], folder[1]), folder[1])
        for file in sorted(file_names["files"]):
            files_list += "<div onclick=\"playTrack('{1}')\">{0}</div>\r\n".format(file[1],
                        re.sub("'", "\\'", os.path.join(file[0], file[1])))
        response.set_attribute("files", files_list)
        return response