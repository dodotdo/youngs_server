import base64
import traceback

import sys
import time as ptime
import urllib.request, urllib.parse, urllib.error

import os
from flask import current_app
from flask_login import current_user
from youngs_server.youngs_app import hash_mod, db
from youngs_server.youngs_app import log
from youngs_server.customlib.flask_restful import abort

from sqlalchemy import exc
from werkzeug.utils import secure_filename
import urllib.parse

from PIL import Image


def save_json_image(save_path_config, url_image_raw):
    try:
        up = urllib.parse.urlparse(url_image_raw)
        head, data = up.path.split(',', 1)
        bits = head.split(';')
        mime_type = bits[0] if bits[0] else 'text/plain'
        charset, b64 = 'ASCII', False
        for bit in bits:
            if bit.startswith('charset='):
                charset = bit[8:]
            elif bit == 'base64':
                b64 = True

        image_file = str.encode(data)
        log.info(image_file[:10])

        hash_mod.update(str(ptime.time()).encode('utf-8'))
        image_filename = hash_mod.hexdigest()[:10]
        filedir = current_app.config[save_path_config]
        if not os.path.exists(filedir):
            os.makedirs(filedir)

        ext = 'jpg'
        filename = secure_filename(image_filename) + '.' + ext

        filepath = os.path.join(filedir, filename)
        # not exist
        if not os.path.exists(filepath):
            with open(filepath, "wb") as message_file:
                message_file.write(base64.decodebytes(image_file))

        file_dir, filename = os.path.split(filepath)
        return filename
    except ValueError as e:
        abort(406, message='wrong image')


def generate_image_url(folder, image_filename):
    image_url = current_app.config['BASE_SERVER'] + '/static/' + folder + '/' + image_filename
    return image_url


def create_thumbnail(signage_id, image_filename, size):
    filedir = current_app.config['SIGNAGE_IMAGE_FOLDER']
    if not os.path.exists(filedir):
        os.makedirs(filedir)

    filepath = os.path.join(filedir, image_filename)
    im = Image.open(filepath)
    im.thumbnail(size)
    filepath, ext = os.path.splitext(filepath)
    filename = filepath.split('/')[-1] + ".thumbnail.jpg"
    im.save(filepath + ".thumbnail.jpg", "JPEG")

    return filename