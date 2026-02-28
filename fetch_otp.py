import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import re
import os
from dotenv import load_dotenv

load_dotenv()

def get_latest_otp():
    try:
        # Load the credentials from the environment
        cred_info = {
            'token': os.environ.get('GMAIL_TOKEN'),
            'refresh_token': os.environ.get('GMAIL_REFRESH_TOKEN'),
            'token_uri': 'https://oauth2.googleapis.com/token',
            'client_id': os.environ.get('GMAIL_CLIENT_ID'),
            'client_secret': os.environ.get('GMAIL_CLIENT_SECRET'),
            'scopes': ['https://www.googleapis.com/auth/gmail.modify']
        }
        
        creds = Credentials.from_authorized_user_info(cred_info)
        service = build('gmail', 'v1', credentials=creds)
        
        sender_email = 'ezone@shardauniversity.com'
        query = f'from:{sender_email}'
        
        # Get the latest message
        results = service.users().messages().list(userId='me', q=query, maxResults=1).execute()
        messages = results.get('messages', [])
        
        if messages:
            message = service.users().messages().get(userId='me', id=messages[0]['id'], format='full').execute()
            
            # Get message parts
            payload = message.get('payload', {})
            parts = payload.get('parts', [])
            
            body = ''
            if 'body' in payload and 'data' in payload['body']:
                body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
            else:
                for part in parts:
                    if part['mimeType'] == 'text/plain':
                        if 'data' in part['body']:
                            body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                            break
            
            # Look for OTP
            otp_match = re.search(r'(\d{6})', body)
            if otp_match:
                otp = otp_match.group(1)
                print(f'✅ OTP Found via API: {otp}')
                return otp
                
        print('❌ OTP not found in email.')
        return None
        
    except Exception as e:
        print(f"❌ Error fetching OTP: {e}")
        return None

if __name__ == "__main__":
    get_latest_otp()
