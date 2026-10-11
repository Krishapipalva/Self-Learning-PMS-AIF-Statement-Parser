"""Download PDF attachments from unread Gmail messages over IMAP SSL.

For a quick personal-account proof of concept. Use a dedicated test mailbox,
synthetic statements, and an app password; never put credentials in source control.
"""
from __future__ import annotations
import imaplib
import os
from pathlib import Path
from email import policy
from email.parser import BytesParser
import re
import sys
from datetime import datetime, timezone
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOWNLOAD_DIR = ROOT / "data" / "incoming"


def safe_filename(name: str) -> str:
    # Discard directory components and replace characters unsafe in filenames.
    name = Path(name or "statement.pdf").name
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._")
    return name or "statement.pdf"


def download_pdf_attachments() -> list[Path]:
    load_dotenv(ROOT / ".env")
    email_address = os.getenv("GMAIL_ADDRESS", "").strip()
    app_password = os.getenv("GMAIL_APP_PASSWORD", "").replace(" ", "").strip()
    mailbox = os.getenv("GMAIL_MAILBOX", "INBOX").strip() or "INBOX"
    search_mode = os.getenv("GMAIL_SEARCH", "UNSEEN").strip().upper()
    output_dir = Path(os.getenv("GMAIL_DOWNLOAD_DIR", str(DEFAULT_DOWNLOAD_DIR)))
    output_dir.mkdir(parents=True, exist_ok=True)

    if not email_address or not app_password:
        raise RuntimeError(
            "Missing Gmail credentials. Copy .env.example to .env and set GMAIL_ADDRESS and GMAIL_APP_PASSWORD."
        )
    if search_mode not in {"UNSEEN", "ALL"}:
        raise ValueError("GMAIL_SEARCH must be either UNSEEN or ALL.")

    client = None
    saved: list[Path] = []
    try:
        print("Connecting to imap.gmail.com:993 over SSL ...")
        client = imaplib.IMAP4_SSL("imap.gmail.com", 993, timeout=25)
        client.login(email_address, app_password)
        status, _ = client.select(mailbox, readonly=True)
        if status != "OK":
            raise RuntimeError(f"Could not open mailbox: {mailbox}")
        print(f"Authenticated and opened mailbox '{mailbox}' in read-only mode.")

        status, data = client.search(None, search_mode)
        if status != "OK":
            raise RuntimeError("Gmail search failed.")
        message_ids = data[0].split() if data and data[0] else []
        print(f"Messages matching {search_mode}: {len(message_ids)}")
        if not message_ids:
            print("No matching messages. Email the test PDF to this account and leave the email unread, then run again.")
            return []

        # Process at most the 25 newest matching messages in this first prototype.
        for message_id in message_ids[-25:]:
            fetch_status, fetch_data = client.fetch(message_id, "(RFC822)")
            if fetch_status != "OK":
                print(f"WARNING: Could not fetch message id {message_id.decode(errors='ignore')}.")
                continue
            raw_message = next(
                (item[1] for item in fetch_data if isinstance(item, tuple) and len(item) > 1 and isinstance(item[1], bytes)),
                None,
            )
            if not raw_message:
                continue
            message = BytesParser(policy=policy.default).parsebytes(raw_message)
            subject = str(message.get("subject", "(no subject)"))
            msg_id_text = message_id.decode(errors="ignore")
            print(f"Checking message {msg_id_text}: {subject[:100]}")
            for part in message.walk():
                if part.is_multipart():
                    continue
                filename = part.get_filename()
                content_type = part.get_content_type()
                if content_type != "application/pdf" and not (filename and filename.lower().endswith(".pdf")):
                    continue
                payload = part.get_payload(decode=True)
                if not payload:
                    print("WARNING: Found a PDF part without downloadable content.")
                    continue
                clean_name = safe_filename(filename or "statement.pdf")
                timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
                target = output_dir / f"msg{msg_id_text}_{timestamp}_{clean_name}"
                # Avoid overwriting if a message is encountered twice.
                counter = 1
                while target.exists():
                    target = output_dir / f"msg{msg_id_text}_{timestamp}_{counter}_{clean_name}"
                    counter += 1
                target.write_bytes(payload)
                saved.append(target)
                print(f"  SAVED PDF: {target}")

        if not saved:
            print("Connected successfully, but no PDF attachments were found in matching messages.")
        return saved
    except imaplib.IMAP4.error as exc:
        raise RuntimeError(
            "Gmail IMAP login/search failed. Check the email address, app password, 2-Step Verification, and account policy."
        ) from exc
    finally:
        if client is not None:
            try:
                client.logout()
            except Exception:
                pass


def main() -> int:
    try:
        saved = download_pdf_attachments()
        print(f"\nFinished. PDF attachment(s) downloaded: {len(saved)}")
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
