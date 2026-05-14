import os
import sys

import resend

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def main() -> int:
    api_key = os.getenv("RESEND_API_KEY", "").strip()
    if not api_key:
        print("Missing RESEND_API_KEY")
        return 1

    resend.api_key = api_key

    try:
        result = resend.Emails.send(
            {
                "from": "unisg@updates.usestartup.dev",
                "to": ["boissieraleksandra@gmail.com"],
                "subject": "hello world",
                "text": "hello world",
            }
        )
        print(f"Email sent successfully. id={result['id']}")
        return 0
    except Exception as exc:
        print(f"Error sending email: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
