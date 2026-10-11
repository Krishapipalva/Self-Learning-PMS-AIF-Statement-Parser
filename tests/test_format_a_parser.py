from pathlib import Path
from app.pdf_extractor import extract_pdf_text

ROOT = Path(__file__).resolve().parents[1]


def test_sample_pdf_contains_expected_fields():
    text = extract_pdf_text(ROOT / "sample_statements" / "format_a_example_wealth.pdf")
    for expected in [
        "Example Wealth Management",
        "TEST-CLIENT-001",
        "Infosys Ltd",
        "Reliance Industries Ltd",
        "500.00",
    ]:
        assert expected in text
