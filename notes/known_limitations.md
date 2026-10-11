# Known limitations (update honestly as implementation evolves)

- The current PDF extractor reads selectable text only; scanned/image-only PDFs need OCR.
- Password-protected PDFs are not decrypted by the current prototype; they should be marked for manual review.
- Gmail access uses an app password through IMAP for a personal test mailbox. OAuth/Gmail API integration would be a more production-oriented authentication path.
- The current ingestion pass scans at most the 25 newest matching messages and does not yet persist a processed-message ledger.
- PDF tables may extract in an unexpected order depending on layout; values must be validated against the document and expected output.
- The one-time LLM format learner, deterministic parser, unified schema validation, and review dashboard/CLI are not implemented in today's starter.
