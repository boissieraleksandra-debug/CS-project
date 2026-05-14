"""
mailer.py — sending the app's transactional emails.

Two modes, picked automatically:

1. **Real send** via Brevo (https://brevo.com) when BREVO_API_KEY
   is set in the environment / .env file. Brevo has a free tier
   (300 emails/day) and works with single-sender verification.

2. **Simulated** when no API key is set. The email body is written
   only to the `emails_log` table; the in-app "Inbox" panel inside
   ui.sidebar() shows them so we can demo without internet.

Either way every send is logged.
"""
#The task of this page is to send emails from an app such that we don't have to have our own domain.
#We used Brevo as the external email service by creating an API key there. It allows us to send actual emails to the users.
#If we had to send more than 300 emails per day (limit on Brevo) then the email content would just be saved on the database instead of sending it.

import os
from typing import Optional, Tuple

# .env support — silently skip if dotenv isn't installed yet.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from db import log_email #Here it imports the email loggin function from the database such that every attempt is recorded.

#This function is called when an email needs to be sent. It gets the recipient's email, the email's subject and the body text.
#And then it sees if there's an API key otherwise just saves in the db.
def send_email(to_email: str, subject: str, body: str) -> Tuple[bool, Optional[str]]:
    """Send an email. Returns (ok, error_message)."""
    #the following 3 lines read values from the .env file and look for the API key and returns just an empty str if it doesn't exist instead of crashing out.
    api_key = os.getenv("BREVO_API_KEY", "").strip()
    from_email = os.getenv("FROM_EMAIL", "").strip()
    from_name = os.getenv("FROM_NAME", "Gigly").strip()

    # ----- Simulated mode -----
    # If no API key is set, then just log to the database and pretend it sent -> sent_ok= true.
    if not api_key:
        log_email(to_email, subject, body, sent_ok=True, error=None)
        return True, None

    # ----- Real send via Brevo -----
    try:
        import sib_api_v3_sdk
        from sib_api_v3_sdk.rest import ApiException

        # Configure the API client with our key
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = api_key
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

        # Brevo wants HTML; convert plain-text \n to <br>
        html_body = body.replace("\n", "<br>\n")

        # Build the email payload
        email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": to_email}],
            sender={"email": from_email, "name": from_name},
            subject=subject,
            html_content=html_body,
        )

        # Send and log success
      
        api_instance.send_transac_email(email)
        log_email(to_email, subject, body, sent_ok=True, error=None)
        return True, None
    
    #Here, instead of crashing down if the content inside try fails (wrong API or no Intenet for ex) then it jumps to this exception.
    #If something went wrong, then the error message is stored in e.
    except Exception as e:
        # Send failed — log the error so we can debug
        log_email(to_email, subject, body, sent_ok=False, error=str(e))
        return False, str(e)
