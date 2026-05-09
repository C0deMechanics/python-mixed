import os


from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
from flask import send_file
from io import BytesIO


SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]


def getGDriveAuthServ():
	gDriveCreds = None
	
	if os.path.exists("auth.json"):
			gDriveCreds = Credentials.from_authorized_user_file("auth.json", SCOPES)
			
	# If there are no (valid) credentials available, let the user log in.
	if not gDriveCreds or not gDriveCreds.valid:
		if gDriveCreds and gDriveCreds.expired and gDriveCreds.refresh_token:
			gDriveCreds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file("cred.json", SCOPES)
			gDriveCreds = flow.run_local_server(port=5050, access_type='offline', prompt='consent')
			
		#print(gDriveCreds.to_json())
		# Save the credentials for the next run
		with open("auth.json", "w") as token:
			token.write(gDriveCreds.to_json())

	service = build("drive", "v3", credentials=gDriveCreds)
	return service


def getFileList():
    try:

        service = getGDriveAuthServ()
        
        results = service.files().list(pageSize=100, fields="nextPageToken, files(id, name, mimeType, parents)").execute()
        
        items = results.get('files', [])

        resultList = []

        cnt = 0

        for item in items:
            cnt = cnt + 1
            resultList.append({"No":cnt, "Name":item['name'], "ID": item['id'], "MimeType": item['mimeType']})

        return resultList
    
    except HttpError as err:
        print(err)


def getFile(file_id):
    try:
        service = getGDriveAuthServ()
        meta = service.files().get(fileId=file_id, fields="mimeType, name").execute()
        mime_type = meta.get("mimeType", "application/octet-stream")
        filename = meta.get("name", "file")

        request = service.files().get_media(fileId=file_id)

        file_raw = BytesIO()
        downloader = MediaIoBaseDownload(file_raw, request)

        done = False
        while not done:
            _, done = downloader.next_chunk()

        file_raw.seek(0)

        return send_file(
            file_raw,
            mimetype=mime_type,
            as_attachment=False,
            download_name=filename
        )

    except Exception as e:
        return {"status": "error", "message": str(e)}



# getFileList()