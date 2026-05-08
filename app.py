## Simple Flask App (app.py)
from flask import Flask, jsonify

import gdrive

app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello World'


@app.route('/filelist')
def filelist():
    itemlist = gdrive.getFileList();
    return jsonify({"fileliest": itemlist})

if __name__ == '__main__':
  app.run()
        