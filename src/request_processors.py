
import os
import importlib.machinery as imp

APPS_RELATIVE_PATH = "apps/" # don't forget the trailing slash
APPS_ABSOLUTE_PATH = os.path.join(os.path.dirname(__file__), APPS_RELATIVE_PATH)

"""
Predefined request processors.
format:
url_path: [app_dir, servlet_class_name]
app_dir - directory in apps folder where the module to handle the request is stored.
"""
PROCESSORS = {
    "/": ["main", "MainServlet"],
    "/main": ["main", "MainServlet"],
}

def get_processor(request):
    requested_page = request.get_requested_page()
    if request.get_header("Referer") is not None:
        host = request.get_header("Host")
        referer = request.get_header("Referer")[len("http://" + host):]
    for app in PROCESSORS:
        processor_exists = app.endswith("*") and requested_page.startswith(app[:-1]) \
            or app == requested_page \
            or app + "/" == requested_page
        if "referer" in locals():
            processor_exists = processor_exists or app == referer or app + "/" == referer
        if processor_exists:
            module_name = PROCESSORS[app][1]
            class_name = module_name
            module_dir = os.path.join(APPS_ABSOLUTE_PATH, PROCESSORS[app][0])
            path_to_module = os.path.join(module_dir, module_name + ".py")
            try:
                loader = imp.SourceFileLoader(module_name, path_to_module)
                module = loader.load_module(module_name)
            except FileNotFoundError:
                print("Cannot find module [{0}]".format(module_name))
                break
            try:
                processor = getattr(module, class_name)()
            except AttributeError:
                print("Cannot find processor in module [{0}]".format(module_name))
                break
            return processor
    return None
