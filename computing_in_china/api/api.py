"""
Code in large parts taken from:
    https://docs.faculty.ai/user-guide/apps/flask_apis/flask_file_upload_download.html
"""
import os

from flask import Flask, request, abort, send_from_directory
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
import yaml

with open("config.yml", "r") as r:
    CFG = yaml.load(r)

UPLOAD_DIRECTORY = CFG["UPLOAD_DIRECTORY"]
DOWNLOAD_DIRECTORY = CFG["DOWNLOAD_DIRECTORY"]
USER = CFG["USER"]
KEY = CFG["KEY"]

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


app = Flask(__name__)

@auth.verify_password
def verify_password(username, password):
    if username == USER and password == KEY:
        return True
    return False


@app.route('/dist/<path:path>')
def send_dist(path):
    return send_from_directory("page/dist", path)
 
@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory("page/assets", path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory("page/js", path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory("page/css", path)

@app.route('/')
def main():
    return send_from_directory("page", "index.html")

@app.route("/files/<path:path>")
@auth.login_required
def get_file(path):
    """Download a file."""
    return send_from_directory(DOWNLOAD_DIRECTORY, path, as_attachment=True)


#@app.route("/files/<filename>", methods=["POST"])
#@auth.login_required
def post_file(filename):
    """Upload a file."""

    if "/" in filename:
        # Return 400 BAD REQUEST
        abort(400, "no subdirectories directories allowed")

    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
        fp.write(request.data)

    # Return 201 CREATED
    return "", 201


if __name__ == "__main__":
    app.run(debug=True, port=8000)
