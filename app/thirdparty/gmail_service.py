from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]


class GmailAPIService:
    def __init__(self):
        self.creds = self.authenticate_gmail()
        self.service = build("gmail", "v1", credentials=self.creds)

    def authenticate_gmail(self):
        """Authenticate and return Gmail API service credentials."""
        creds = None
        token_path = "./app/config/token.json"
        credentials_path = "./app/config/credentials.json"
        credentials_updated = False  # Track if credentials have changed

        # Check for existing token.json file
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
        # Refresh or re-authenticate if credentials are not valid
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                credentials_updated = True
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
                credentials_updated = True

        # Save the credentials only if they have been updated
        if credentials_updated:
            with open(token_path, "w") as token_file:
                token_file.write(creds.to_json())

        return creds



    async def get_unread_emails(self):
        """Fetch unread messages and send dummy replies."""
        results = (
            self.service.users()
            .messages()
            .list(
                userId="me",
                q="is:unread",
                maxResults=5,
            )
            .execute()
        )
        messages = results.get("messages", [])

        if not messages:
            return {"response": "No new messages found.", "status_code": 200}

        for message in messages:
            # Get the email details
            msg = (
                self.service.users()
                .messages()
                .get(userId="me", id=message["id"])
                .execute()
            )
            headers = msg["payload"]["headers"]
            subject = next(
                header["value"] for header in headers if header["name"] == "Subject"
            )
            from_email = next(
                header["value"] for header in headers if header["name"] == "From"
            )

            from_email = from_email.split("<")[-1].strip(">")

            print(f"Processing message from: {from_email} | Subject: {subject}")

            # Send a reply
            # send_reply(service, from_email, subject)

        return {"response": "Unread Emails Fetched Successfully", "status_code": 200}

    async def send_reply(self, to_email, subject):
        reply_text = "This is an automated reply. Thank you for reaching out!"

        message = MIMEText(reply_text)
        message["to"] = to_email
        message["subject"] = f"Re: {subject}"

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")

        self.service.users().messages().send(
            userId="me", body={"raw": raw_message}
        ).execute()
        return {"response": "Reply sent successfully", "status_code": 200}

    async def gmail_health_check(self):
        try:
            self.service.users().getProfile(userId="me").execute()
            return {"status_code": 200, "data": "Gmail API is working correctly."}
        except Exception as e:
            return {"status_code": 500, "data": f"Error in gmail_health_check: {e}"}
