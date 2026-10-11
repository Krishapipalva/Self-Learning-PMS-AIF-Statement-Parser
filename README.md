# Activv Money PMS/AIF Statement Parser - Day 1 Starter

This is a small proof of concept for today's target: (1) read a synthetic PDF locally, then (2) connect to a dedicated test Gmail inbox and save PDF attachments. It is not the complete assignment yet.

## What is included

- `sample_statements/format_a_example_wealth.pdf`: fictional, selectable-text sample PMS statement.
- `app/pdf_extractor.py`: extracts selectable text from a PDF and saves a `.txt` file.
- `app/gmail_ingestion.py`: logs into Gmail IMAP over SSL in read-only mode and downloads PDF attachments from matching messages.
- `.env.example`: credential template. Keep your real `.env` private.
- `notes/`: starter notes for design, limitations, and AI usage.

## Requirements

- Python 3.10 or later recommended.
- A dedicated test Gmail account, preferably with no personal or real client mail.
- For IMAP app-password authentication, Google requires 2-Step Verification and may not offer app passwords for some managed or protected accounts. Never use your regular Gmail password here.

## A. Setup on Windows PowerShell

Open PowerShell in this project folder:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use Command Prompt instead and run:

```bat
.venv\Scripts\activate.bat
```

## B. Prove PDF extraction works first

Run:

```powershell
python -m app.pdf_extractor sample_statements/format_a_example_wealth.pdf
```

Expected result:
- The command prints `SUCCESS: extracted text...`.
- It writes `output/extracted_text/format_a_example_wealth.txt`.
- The preview should include `Example Wealth Management`, `TEST-CLIENT-001`, `Infosys Ltd`, `Reliance Industries Ltd`, and the dividend transaction of `500.00`.

Open the generated `.txt` and compare its values with the PDF. This validates text extraction, not yet perfect table-to-JSON parsing.

## C. Prepare a safe Gmail test

1. Use a dedicated test account. Do not use real client statements.
2. Open your Google Account security settings and turn on 2-Step Verification if it is appropriate for that account.
3. If the account offers App Passwords, create a new app password for this prototype. If App Passwords are unavailable (common for some school/work-managed accounts or Advanced Protection), do not disable security; use a separate test account or implement the Gmail API/OAuth path instead.
4. Copy `.env.example` to `.env` in this folder:

```powershell
Copy-Item .env.example .env
notepad .env
```

5. Fill `GMAIL_ADDRESS` and `GMAIL_APP_PASSWORD`. You can paste the 16-character app password with or without spaces. Do not send it to anyone, paste it into ChatGPT, or commit `.env`.
6. Email `sample_statements/format_a_example_wealth.pdf` as an attachment to that test account. Use a subject such as `PMS Statement - Format A - Synthetic Test`.
7. Leave that message unread in the test account. The default search is `UNSEEN`.

## D. Prove Gmail ingestion works

Run:

```powershell
python -m app.gmail_ingestion
```

Successful output should confirm it connected to `imap.gmail.com:993`, opened `INBOX` in read-only mode, reported matching messages, and printed `SAVED PDF: ...` for the attachment.

The script does not mark messages read or delete them. It downloads only PDF attachments from up to the 25 newest matching messages. In this first version, running it again may download an attachment again under a new timestamped filename.

If you see `Missing Gmail credentials`, check that `.env` is in the project root and both fields are filled. If login fails, do not share the password in a support request. Check the account's app-password eligibility and generate a new app password if needed.

## E. Extract the downloaded attachment

Copy the exact path printed by the previous command and run (example path shown):

```powershell
python -m app.pdf_extractor "data/incoming/msg123_20261010T090000Z_format_a_example_wealth.pdf"
```

The actual filename will differ. This produces a text file in `output/extracted_text/`. Compare it with the sample PDF.

## Today's definition of done

- [ ] Python environment installs successfully.
- [ ] Sample PDF is extracted locally and important text/values are present.
- [ ] Synthetic PDF is received as an email attachment in the test mailbox.
- [ ] Gmail ingestion logs in and saves the attachment without deleting or marking the email read.
- [ ] The downloaded attachment can also be extracted with `pdf_extractor.py`.
- [ ] Add screenshots/terminal output to your own notes (never include credentials).

## Not implemented yet

Today's starter does not yet learn new formats with an LLM, save extraction rules, deterministically parse holdings/transactions into JSON, reconcile totals, or handle scanned/password-protected PDFs. Those are the next development steps.
