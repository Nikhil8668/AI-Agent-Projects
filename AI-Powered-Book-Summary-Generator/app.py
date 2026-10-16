from flask import Flask , render_template , request , redirect , url_for , flash
from werkzeug.utils import secure_filename
import os 
from dotenv import load_dotenv

# Google API imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

#UPLOAD FOLDER setup
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER , exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Allowed File Types (n8n workflow uses "Extract From PDF", so PDF only)
ALLOWED_EXTENSIONS = {'pdf'}

#Google Drive config
OAUTH_CLIENT_FILE = os.getenv("OAUTH_CLIENT_FILE", "oauth_client.json")
TOKEN_FILE = "token.json"
SCOPES = ["https://www.googleapis.com/auth/drive"]
TARGET_FOLDER_ID = os.getenv("TARGET_FOLDER_ID", "")

def allowed_file(filename):
    return "." in filename and filename.rsplit("." , 1)[1].lower() in ALLOWED_EXTENSIONS

def get_credentials():
    """Log in with your Google account (browser opens the first time), then reuse token.json."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(OAUTH_CLIENT_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    return creds

def upload_to_drive(file_path , file_name):
    """Upload a file to Google Drive as the logged-in user."""
    service = build('drive', 'v3', credentials=get_credentials())

    file_metadata = {
        'name' : file_name,
        'parents':[TARGET_FOLDER_ID]
    }

    media = MediaFileUpload(file_path , resumable=True)

    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()


    print(f" Uploaded to Drive wiht file ID : {uploaded_file.get('id')}")
    return uploaded_file.get('id')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload',methods=['POST'])
def upload_file():
    if 'bookfile' not in request.files:
        flash("No file part")
        return redirect(url_for('index'))

    file = request.files['bookfile']

    if file.filename == "":
        flash("No selected file")
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Upload PDF to Google Drive; the n8n workflow picks it up and creates the summary
        upload_to_drive(file_path , filename)

        flash(f"'{filename}' uploaded! The summary will appear in Drive in a minute or two.")
        return redirect(url_for('index'))

    flash("File type not allowed.")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)