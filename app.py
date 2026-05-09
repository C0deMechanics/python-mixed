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

@app.route('/viewfile/<fileid>', methods=['GET'])
def viewfile(fileid):
  return gdrive.getFile(fileid)

if __name__ == '__main__':
  app.run()
        