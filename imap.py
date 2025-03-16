import imaplib

IMAP_SERVER = "imap.gmail.com"
EMAIL = "2023497222.harsh@ug.sharda.ac.in"
APP_PASSWORD = "caej hdte trrl bydy"

try:
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, APP_PASSWORD)
    print("✅ IMAP Login Successful!")
except imaplib.IMAP4.error as e:
    print("❌ IMAP Login Failed:", e)
