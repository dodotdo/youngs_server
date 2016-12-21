from flask import current_app


def generate_content_url(folder, content_filename):
    content_url = current_app.config['BASE_SERVER'] + '/res/webview/' + folder + '/' + content_filename
    return content_url



def generate_image_url(folder, image_filename):
    image_url = current_app.config['BASE_SERVER'] + '/res/image/' + folder + '/' + image_filename
    return image_url
