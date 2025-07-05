
import pandas as pd
import pdfplumber
from bs4 import BeautifulSoup
import re
import os

# --- Step 1: Extract and clean text from a sample PDF ---
pdf_path = "sample_regulatory_document.pdf"  # Replace with actual file
extracted_text = []

if os.path.exists(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                # Remove headers/footers/disclaimers
                cleaned = re.sub(r"(?i)(page\s+\d+|confidential|disclaimer.*)", "", text)
                cleaned = re.sub(r"\n{2,}", "\n", cleaned).strip()
                extracted_text.append({
                    "chunk_id": f"PDF-{i+1}",
                    "source_url": "https://example.gov/sample.pdf",
                    "document_type": "PDF",
                    "clean_text": cleaned,
                    "date_issued": "2023-01-01"
                })
else:
    # Fallback sample text if no PDF present
    extracted_text.append({
        "chunk_id": "PDF-1",
        "source_url": "https://example.gov/sample.pdf",
        "document_type": "PDF",
        "clean_text": "This is a simulated section of regulatory text from the FDA guidance documents.\n\nSection 1. Introduction\nThis guidance provides...",
        "date_issued": "2023-01-01"
    })

# --- Step 2: Extract and clean from sample HTML ---
html_sample = """
<html>
<head><title>FDA Regulation 123</title></head>
<body>
<h1>Introduction</h1>
<p>This document outlines compliance standards...</p>
<footer>Page 1 - FDA.gov</footer>
</body>
</html>
"""

soup = BeautifulSoup(html_sample, "html.parser")
main_text = soup.get_text(separator="\n")
main_text = re.sub(r"(?i)(page\s+\d+|fda\.gov|footer.*)", "", main_text).strip()

extracted_text.append({
    "chunk_id": "HTML-1",
    "source_url": "https://www.ecfr.gov/example",
    "document_type": "HTML",
    "clean_text": main_text,
    "date_issued": "2023-02-01"
})

# --- Step 3: Save structured dataset ---
df = pd.DataFrame(extracted_text)
df.to_csv("sample_cleaned_output.csv", index=False)

# --- Step 4: Save explanation file ---
readme = """
This is a sample output of a regulatory data extraction and cleaning tool.

Files included:
- sample_cleaned_output.csv: Structured chunks of text extracted from simulated PDF and HTML sources, with metadata.
- README.txt: Description of process.

Metadata columns:
- chunk_id: Unique text section ID
- source_url: Origin of the content
- document_type: PDF or HTML
- clean_text: Extracted and cleaned section content
- date_issued: Document date
"""
with open("README.txt", "w") as f:
    f.write(readme.strip())

print("✅ Sample regulatory dataset created.")
