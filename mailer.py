"""
mailer.py — sending the app's transactional emails.

Two modes, picked automatically:

1. **Real send** via Resend when RESEND_API_KEY is set in the
   environment / .env file.

2. **Simulated** when no API key is set. The email body is written
   only to the `emails_log` table; the in-app "Inbox" panel inside
   ui.sidebar() shows them so we can demo without internet.

Either way every send is logged.
"""

import os
from typing import Optional, Tuple

# .env support — silently skip if dotenv isn't installed yet.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from db import log_email


def _format_from_address(from_email: str, from_name: str) -> str:
    if from_name:
        return f"{from_name} <{from_email}>"
    return from_email


def send_email(to_email: str, subject: str, body: str) -> Tuple[bool, Optional[str]]:
    """Send an email. Returns (ok, error_message)."""
    api_key = os.getenv("RESEND_API_KEY", "").strip()
    from_email = os.getenv("FROM_EMAIL", "").strip()
    from_name = os.getenv("FROM_NAME", "Gigly").strip()

    if not api_key:
        log_email(to_email, subject, body, sent_ok=True, error=None)
        return True, None

    try:
        import resend

        if not from_email:
            raise ValueError("Missing FROM_EMAIL")

        resend.api_key = api_key
        result = resend.Emails.send(
            {
                "from": _format_from_address(from_email, from_name),
                "to": [to_email],
                "subject": subject,
                "html": body.replace("\n", "<br>\n"),
                "text": body,
            }
        )
        if not result.get("id"):
            raise RuntimeError("Resend did not return an email id")

        log_email(to_email, subject, body, sent_ok=True, error=None)
        return True, None
    except Exception as e:
        log_email(to_email, subject, body, sent_ok=False, error=str(e))
        return False, str(e)
