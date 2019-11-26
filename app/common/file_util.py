import os

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'static', 'tmp')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['md']
