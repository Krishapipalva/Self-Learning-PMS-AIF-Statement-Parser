# Design note (working draft)

## Today's prototype scope
- Retrieve PDF attachments from a dedicated test Gmail account via IMAP over SSL.
- Parse selectable text from PDFs with pdfplumber.
- Save extracted text for later deterministic parsing.
- Use only synthetic sample data.

## Assumptions
- Today's sample PDF is text-based, not scanned.
- Initial mail search targets unread messages in INBOX.
- Password-protected files and image-only PDFs are documented as limitations for this prototype, rather than being silently accepted.

## Next step
Add format fingerprints, one-time LLM-generated extraction configuration, deterministic parser execution, field-level validation, and tests that prove known-format runs make zero LLM calls.
