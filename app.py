## Simple Flask App (app.py)
from flask import Flask, jsonify, request

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

@app.route('/fileuploader')
def fileuploader():
  return ''' 
  <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Upload</title>
</head>
<body style="background:#f5f5f5;">
<form method="POST" enctype="multipart/form-data"
      action="/upload"
      style="max-width: 420px; margin: 80px auto; padding: 25px; border-radius: 10px; background: #ffffff; box-shadow: 0 4px 12px rgba(0,0,0,0.1); font-family: Arial;">
<h4 style="text-align: center; margin-bottom: 20px;">Upload to Google Drive</h4>
<input type="file" name="file"
       style="width: 100%; margin-bottom: 20px;">

<button type="submit"
        style="width: 100%; padding: 10px; border: none; border-radius: 5px; background-color: #007bff; color: white; font-weight: bold; cursor: pointer;">
    Upload
</button>
</form>

</body>
</html>
  '''

@app.route('/upload', methods=['POST'])
def upload():
  fileid = gdrive.uploadfile(request)
  return f'file successfully added file {fileid}.'


@app.route('/filedeleter')
def filedeleter():
  return '''
  <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Delete File</title>
</head>
<body style="background:#f5f5f5;">
<form method="POST"
      action="/delete"
      style="max-width: 420px; margin: 80px auto; padding: 25px; border-radius: 10px; background: #ffffff; box-shadow: 0 4px 12px rgba(0,0,0,0.1); font-family: Arial;">
    <h4 style="text-align: center; margin-bottom: 20px;">Delete File from Google Drive</h4>
    <input type="text" name="file_id" placeholder="Enter File ID"
           style="width: 100%; padding: 10px; margin-bottom: 20px; border: 1px solid #ccc; border-radius: 5px;">
    <button type="submit"
            style="width: 100%; padding: 10px; border: none; border-radius: 5px; background-color: #dc3545; color: white; font-weight: bold; cursor: pointer;">
        Delete
    </button>
</form>
</body>
</html>
  '''

@app.route('/delete', methods=['POST'])
def delete():
  file_id = request.form.get('file_id')
  return gdrive.deletefile(file_id)


if __name__ == '__main__':
  app.run()
        