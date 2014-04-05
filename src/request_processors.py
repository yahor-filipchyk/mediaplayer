
import os
import importlib.machinery as imp

APPS_RELATIVE_PATH = "apps/" # don't forget the trailing slash
APPS_ABSOLUTE_PATH = os.path.join(os.path.dirname(__file__), APPS_RELATIVE_PATH)

"""
Predefined request processors.
format:
url_path: [app_dir, module_name, function]
app_dir - directory in apps folder where the module to handle the request is stored.
function - the function to be executed to handle client request. Takes the http_request object
and returns the http_response object.
"""
PROCESSORS = {
    "/": ["", "main_page", "handle_request"],
    "/main*": ["main", "main_page", "handle_request"],
}

def get_processor(requested_page):
    for app in PROCESSORS:
        if (app.endswith("*") and requested_page.startswith(app[:-1])) or app == requested_page:
            module_name = PROCESSORS[app][1]
            function_name = PROCESSORS[app][2]
            module_dir = os.path.join(APPS_ABSOLUTE_PATH, PROCESSORS[app][0])
            path_to_module = os.path.join(module_dir, module_name + ".py")
            try:
                loader = imp.SourceFileLoader(module_name, path_to_module)
                module = loader.load_module(module_name)
            except FileNotFoundError:
                print("Cannot find module [{0}]".format(module_name))
                break
            try:
                processor = getattr(module, function_name)
            except AttributeError:
                print("Cannot find processor in module [{0}]".format(module_name))
                break
            return processor
    return None
