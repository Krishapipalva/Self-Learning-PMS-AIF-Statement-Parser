"""Extract selectable text from a PDF using pdfplumber."""
from __future__ import annotations
import argparse
from pathlib import Path
import sys
import pdfplumber

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "output" / "extracted_text"


def extract_pdf_text(pdf_path: Path) -> str:
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a .pdf file, got: {pdf_path.name}")

    page_texts: list[str] = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        if not pdf.pages:
            raise ValueError("The PDF contains no pages.")
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            page_texts.append(f"--- PAGE {page_number} ---\n{text}")
    combined = "\n\n".join(page_texts).strip()
    if not combined:
        raise ValueError(
            "No selectable text was found. This may be a scanned/image-only PDF; OCR support is not included in today's prototype."
        )
    return combined


def save_text(text: str, pdf_path: Path, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{pdf_path.stem}.txt"
    output_path.write_text(text + "\n", encoding="utf-8")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract text from a selectable-text PDF.")
    parser.add_argument("pdf", type=Path, help="Path to a PDF file")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUTPUT, help="Directory for extracted .txt files")
    args = parser.parse_args()
    try:
        text = extract_pdf_text(args.pdf)
        output_path = save_text(text, args.pdf, args.out_dir)
        print(f"SUCCESS: extracted text from {args.pdf}")
        print(f"Saved text to: {output_path}")
        print("\nPreview (first 1,500 characters):\n")
        print(text[:1500])
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
