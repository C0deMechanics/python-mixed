import os

from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


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
			gDriveCreds = flow.run_local_server(port=5050)
			
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


getFileList()