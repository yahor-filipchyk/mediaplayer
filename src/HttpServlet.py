from HttpResponse import HttpResponse
import utils
import os
import mimetypes as mime


class HttpServlet(object):

    def __init__(self, context):
        self.server_context = context
        self.templates_dir = utils.TEMPLATES_FOLDER
        self.static_files_dir = os.path.join(os.path.dirname(__file__), "static/")

    def set_templates_dir(self, templates_dir):
        self.templates_dir = templates_dir

    def set_static_files_dir(self, static_dir):
        self.static_files_dir = static_dir

    def service(self, request):
        """Default behaviour is to send response with 404 error code"""

        response = HttpResponse()
        response.set_response_code(404)
        response.set_response_status("Not found")
        response.set_attribute("error_code", response.http_code)
        response.set_attribute("status", response.response_status)
        response.set_attribute("message", "Requested page <span class=\"page\">{0}</span> was not found."
                               .format(request.get_header("Host") + request.get_requested_resource()))
        response.set_contents(utils.load_template("error_page.html"))
        return response

    def get_file(self, request):
        resource = request.get_requested_page()
        referer = request.get_header("Referer")
        if referer is not None and referer.endswith("/"):
            app_referer = referer[referer[:-1].rfind("/"):-1]
            if resource.startswith(app_referer):
                resource = resource[len(app_referer):]
        file_name = os.path.join(os.path.dirname(self.static_files_dir), resource[1:] if resource.startswith("/") else resource)
        mime_type = mime.guess_type(file_name)
        if os.path.isfile(file_name):
            response = HttpResponse()
            file = open(file_name, "rb")
            file_contents = bytearray(file.read())
            response.set_contents(file_contents)
            response.set_header("Content-Type", mime_type[0])
            file.close()
            return response
        else:
            return self.service(request)