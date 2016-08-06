import base64
import time as ptime

import os
from flask import current_app
from youngs_server.youngs_app import hash_mod, log
from werkzeug.utils import secure_filename


def save_html(folder, content):

    hash_mod.update(str(ptime.time()).encode('utf-8'))
    image_filename = hash_mod.hexdigest()[:10]

    ext = 'html'
    filename = secure_filename(image_filename) + '.' + ext
    filedir = os.path.join(current_app.config['INROOM_WEBVIEW_FOLDER'], folder)
    if not os.path.exists(filedir):
        os.makedirs(filedir)
    filepath = os.path.join(filedir, filename)
    if not os.path.exists(filepath):
        with open(filepath, "wb") as html_file:
            log.info(content)
            content = str.encode(content)
            html_file.write(content)
    file_dir, filename = os.path.split(filepath)
    return filename

def delete_html(folder, content_filename):
    filedir = os.path.join(current_app.config['INROOM_WEBVIEW_FOLDER'], folder)
    if not os.path.exists(filedir):
        os.makedirs(filedir)
    filepath = os.path.join(filedir, content_filename)
    # exist
    if os.path.exists(filepath):
        log.info(os.remove(filepath))

