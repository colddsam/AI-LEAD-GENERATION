import imaplib
import email
from email.header import decode_header
from typing import List, Tuple
from app.config import get_settings
settings = get_settings()
import logging

logger = logging.getLogger(__name__)

async def fetch_recent_replies(since_minutes: int = 30) -> List[Tuple[str, str]]:
    """
    Connects to the IMAP server and checks for recent replies.
    Returns a list of tuples containing (sender_email, subject).
    """
    if not settings.IMAP_USER or not settings.IMAP_PASSWORD:
        logger.warning("IMAP credentials not set, skipping reply polling.")
        return []

    try:
        mail = imaplib.IMAP4_SSL(settings.IMAP_HOST)
        mail.login(settings.IMAP_USER, settings.IMAP_PASSWORD)
        mail.select("inbox")
        
        # Search for unseen emails (or could use UNSEEN or SINCE)
        status, messages = mail.search(None, "UNSEEN")
        if status != "OK":
            mail.logout()
            return []
            
        email_ids = messages[0].split()
        results = []
        
        for e_id in email_ids[-20:]:  # Process max 20 latest unseen to prevent timeouts
            # Fetch the email
            status, msg_data = mail.fetch(e_id, "(RFC822)")
            if status != "OK":
                continue
                
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Decrypt subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                        
                    sender = msg.get("From")
                    # Extract pure email from 'Name <email@domain.com>'
                    if "<" in sender and ">" in sender:
                        sender = sender.split("<")[1].split(">")[0]
                        
                    results.append((sender.lower().strip(), subject))
        
        mail.logout()
        return results

    except Exception as e:
        logger.error(f"Error checking replies via IMAP: {e}")
        return []
