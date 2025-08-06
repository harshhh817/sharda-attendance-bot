"""OTP Fetcher for Sharda University login."""
import imaplib
import email
import re
import time
from typing import Optional

from .config import config
from .logger import logger

class OTPFetcher:
    """Handles fetching OTP from email for Sharda University login."""
    
    def __init__(self):
        """Initialize the OTP fetcher with configuration."""
        self.imap_server = config.IMAP_SERVER
        self.email = config.EMAIL
        self.app_password = config.APP_PASSWORD
        self.sender_email = config.SENDER_EMAIL
        self.max_retries = 3
        self.retry_delay = 5  # seconds
        
    def fetch_otp(self) -> Optional[str]:
        ""
        Fetch the latest OTP from the email.
        
        Returns:
            str: The OTP if found, None otherwise.
        """
        logger.info("Fetching OTP from email...")
        
        for attempt in range(1, self.max_retries + 1):
            try:
                # Connect to the IMAP server
                mail = imaplib.IMAP4_SSL(self.imap_server)
                mail.login(self.email, self.app_password)
                mail.select("inbox")
                
                # Search for emails from the sender
                status, messages = mail.search(
                    None, 
                    f'(FROM "{self.sender_email}" SUBJECT "OTP")',
                    'UNSEEN'  # Only check unread emails
                )
                
                if status != 'OK':
                    logger.error("Failed to search emails")
                    return None
                
                # Get the latest email ID
                email_ids = messages[0].split()
                if not email_ids:
                    logger.info(f"No OTP emails found (attempt {attempt}/{self.max_retries})")
                    time.sleep(self.retry_delay)
                    continue
                
                latest_email_id = email_ids[-1]
                
                # Fetch the email
                status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
                if status != 'OK':
                    logger.error("Failed to fetch email")
                    return None
                
                # Parse the email
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        email_body = self._get_email_body(msg)
                        
                        # Extract OTP using regex
                        otp = self._extract_otp(email_body)
                        if otp:
                            logger.info(f"OTP found: {'*' * len(otp)}")
                            return otp
                
                logger.info(f"No OTP found in email (attempt {attempt}/{self.max_retries})")
                time.sleep(self.retry_delay)
                
            except Exception as e:
                logger.error(f"Error fetching OTP (attempt {attempt}/{self.max_retries}): {e}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)
                
            finally:
                try:
                    mail.logout()
                except:
                    pass
        
        logger.error("Failed to fetch OTP after maximum retries")
        return None
    
    def _get_email_body(self, msg: email.message.Message) -> str:
        ""Extract the email body from a message.""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    try:
                        return part.get_payload(decode=True).decode()
                    except UnicodeDecodeError:
                        try:
                            return part.get_payload(decode=True).decode('latin-1')
                        except:
                            continue
        else:
            try:
                return msg.get_payload(decode=True).decode()
            except UnicodeDecodeError:
                return msg.get_payload(decode=True).decode('latin-1')
        
        return ""
    
    def _extract_otp(self, text: str) -> Optional[str]:
        ""Extract OTP from text using regex.""
        # Look for 6-digit OTP
        otp_match = re.search(r'\b(\d{6})\b', text)
        if otp_match:
            return otp_match.group(1)
            
        # Alternative pattern if the above doesn't work
        otp_match = re.search(r'(?:OTP|One Time Password)[: ]*(\d{6})', text, re.IGNORECASE)
        if otp_match:
            return otp_match.group(1)
            
        return None

def get_otp() -> Optional[str]:
    ""Convenience function to get OTP."""
    return OTPFetcher().fetch_otp()

if __name__ == "__main__":
    # Test the OTP fetcher
    print("Testing OTP fetcher...")
    otp = get_otp()
    if otp:
        print(f"OTP found: {otp}")
    else:
        print("No OTP found")
