import imaplib
import email
import re

# Your email credentials
EMAIL = "2023497222.harsh@ug.sharda.ac.in"
APP_PASSWORD = "caej hdte trrl bydy"  # Use an App Password, not your actual password
IMAP_SERVER = "imap.gmail.com"
SENDER_EMAIL = "ezone@shardauniversity.com"

def get_latest_otp():
    try:
        # Connect to Gmail's IMAP server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, APP_PASSWORD)
        mail.select("inbox")

        # Search for emails from the specific sender
        result, data = mail.search(None, f'FROM "{SENDER_EMAIL}"')
        email_ids = data[0].split()

        if not email_ids:
            print("❌ No OTP emails found.")
            return None

        # Fetch the latest email
        latest_email_id = email_ids[-1]
        result, msg_data = mail.fetch(latest_email_id, "(RFC822)")

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                email_body = ""

                # Extract email body
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type == "text/plain":
                            email_body = part.get_payload(decode=True).decode()
                            break
                else:
                    email_body = msg.get_payload(decode=True).decode()

                # Extract OTP using regex
                otp_match = re.search(r"(\d{6})", email_body)
                if otp_match:
                    otp = otp_match.group(1)
                    print(f"✅ OTP Found: {otp}")  # Prints OTP
                    return otp

        print("❌ OTP not found in email.")
        return None

    except Exception as e:
        print(f"❌ Error fetching OTP: {e}")
        return None

# Run the function if this script is executed directly
if __name__ == "__main__":
    otp = get_latest_otp()
    if otp:
        print(f"🔢 OTP Retrieved: {otp}")  # Extra print for confirmation
