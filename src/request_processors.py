
import os
import importlib.machinery as imp
from HttpRequest import HttpRequest

APPS_RELATIVE_PATH = "apps/" # don't forget the trailing slash
APPS_ABSOLUTE_PATH = os.path.join(os.path.dirname(__file__), APPS_RELATIVE_PATH)

"""
Predefined request processors.
format:
url_path: [app_dir, servlet_class_name]
app_dir - directory in apps folder where the module to handle the request is stored.
"""
PROCESSORS = {
    "/": ["mediaplayer", "MainPage"],
    "/music": ["mediaplayer", "MediaPlayer"],
    "/music/play": ["mediaplayer", "PlayHandler"],
    "/music/pause": ["mediaplayer", "PauseHandler"],
    "/music/volume": ["mediaplayer", "VolumeHandler"],
    "/video": ["mediaplayer", "MediaPlayer"],
    "/video/play": ["mediaplayer", "PlayHandler"],
    "/video/pause": ["mediaplayer", "PauseHandler"],
    "/video/volume": ["mediaplayer", "VolumeHandler"],
    "/nowplaying": ["mediaplayer", "NowPlaying"],
    "/main": ["main", "MainServlet"],
}

CONTEXT = {}


def get_processor(request):
    requested_page = request.get_requested_page()
    # print(requested_page)
    if request.get_header("Referer") is not None:
        host = request.get_header("Host")
        referer = HttpRequest.extract_requested_page(request.get_header("Referer")[len("http://" + host):])
        # print(referer)
    for app in PROCESSORS:
        processor_exists = app.endswith("*") and requested_page.startswith(app[:-1]) \
            or app == requested_page \
            or app + "/" == requested_page
        if processor_exists:
            return load_module(app)
    for app in PROCESSORS:
        if "referer" in locals() and not processor_exists:
            processor_exists = processor_exists or app == referer or app + "/" == referer
            if processor_exists:
                return load_module(app)
    return None


def load_module(app):
    module_name = PROCESSORS[app][1]
    class_name = module_name
    module_dir = os.path.join(APPS_ABSOLUTE_PATH, PROCESSORS[app][0])
    path_to_module = os.path.join(module_dir, module_name + ".py")
    try:
        loader = imp.SourceFileLoader(module_name, path_to_module)
        module = loader.load_module(module_name)
    except FileNotFoundError:
        print("Cannot find module [{0}]".format(module_name))
        return None
    try:
        processor = getattr(module, class_name)(CONTEXT)
    except AttributeError:
        print("Cannot find processor in module [{0}]".format(module_name))
        return None
    return processor
