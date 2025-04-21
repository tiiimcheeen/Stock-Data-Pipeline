import os
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv
from pathlib import Path
from typing import Union, List
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

def send_email(subject: str, body: str, attachment_path: Union[str, List[str]] = None):
    creds = Credentials.from_authorized_user_file(os.getenv("GMAIL_TOKEN_PATH"))
    service = build("gmail", "v1", credentials=creds)

    message = MIMEMultipart()
    message["to"] = os.getenv("GMAIL_RECEIVER")
    message["from"] = os.getenv("GMAIL_SENDER")
    message["subject"] = subject
    message.attach(MIMEText(body, "plain"))

    paths = [attachment_path] if isinstance(attachment_path, str) else (attachment_path or [])

    for path in paths:
        with open(path, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(path)}"'
            message.attach(part)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": raw_message}).execute()
