import os
import request_processors as rp

MAIN_APP_FOLDER = os.path.join(rp.APPS_ABSOLUTE_PATH, "main/")
TEMPLATES_FOLDER = os.path.join(MAIN_APP_FOLDER, "templates/")

def load_template(template, template_dir=TEMPLATES_FOLDER):
    template_file = os.path.join(template_dir, template)
    with open(template_file, "r") as file:
        return file.read()