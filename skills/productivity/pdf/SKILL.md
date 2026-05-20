---
name: pdf
description: Create, extract text from, render, and review PDF files using open-source tools (reportlab, pdfplumber, pypdf, Poppler).
version: 1.0.0
author: Broville
license: MIT
platforms:
  - linux
trigger:
  - User asks to create, generate, or produce a PDF document
  - User asks to read, extract text, or extract data from a PDF
  - User asks to review, verify, or visually inspect a PDF
  - User asks to render PDF pages to images for layout checking
  - Rendering or layout quality of a document matters
inputs:
  - name: pdf_path
    description: Path to an existing PDF file (for extraction or rendering)
    required: false
  - name: output_dir
    description: Directory for generated or rendered files (defaults to output/pdf/)
    required: false
outputs:
  - name: generated_pdf
    description: Path to the newly created PDF file
  - name: rendered_pages
    description: Paths to PNG images of each rendered PDF page
  - name: extracted_text
    description: Extracted text content from a PDF
metadata:
  hermes:
    tags:
      - pdf
      - document-generation
      - text-extraction
      - visual-review
      - reportlab
      - pdfplumber
    related_skills:
      - screenshot
---

# PDF

Create, extract, render, and review PDF documents. Uses open-source Python libraries and system tools — no proprietary dependencies, no API keys, no cloud services required.

## When to Use

- Creating PDFs programmatically with controlled formatting and layout
- Extracting text or tabular data from existing PDFs
- Rendering PDF pages to PNG for visual inspection before delivery
- Validating that generated PDFs look correct (no broken fonts, clipped text, or layout shifts)

## Prerequisites

Install Python dependencies:

```bash
python3 -m pip install reportlab pdfplumber pypdf
```

Install Poppler for PDF-to-image rendering:

```bash
# Debian/Ubuntu
sudo apt-get install -y poppler-utils

# Fedora
sudo dnf install -y poppler-utils

# Arch Linux
sudo pacman -S poppler
```

Verify Poppler is available:

```bash
pdftoppm -h 2>&1 | head -1
# Expected: usage message showing pdftoppm options
```

## Steps

### 1. Determine the task type

- **Generation** → Use `reportlab` (Step 2)
- **Extraction** → Use `pdfplumber` or `pypdf` (Step 3)
- **Visual review** → Render with `pdftoppm` then inspect (Step 4)
- **Full workflow** → Generate, then render and verify (Steps 2 → 4 → 5)

### 2. Generate a PDF with reportlab

Use the helper script `scripts/generate_pdf.py` or write reportlab code directly:

```bash
python3 scripts/generate_pdf.py --output output/pdf/report.pdf --title "My Report"
```

For custom content, write a Python script using reportlab:

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("output/pdf/report.pdf", pagesize=letter)
c.setFont("Helvetica", 12)
c.drawString(72, 720, "Hello, PDF!")
c.save()
```

Key reportlab guidelines:
- Always set page size explicitly (`letter`, `A4`, or custom tuple)
- Use `Helvetica` or `Times-Roman` (built-in fonts) to avoid embedding issues
- For Unicode text, register a TTF font with `pdfmetrics.registerFont()` and include the font file
- Use `Paragraph` from `reportlab.platypus` for flowing text with proper wrapping

### 3. Extract text or data from a PDF

**Fast text extraction** with `pdfplumber`:

```python
import pdfplumber

with pdfplumber.open("input/document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            print(text)
```

**Table extraction** with `pdfplumber`:

```python
import pdfplumber

with pdfplumber.open("input/document.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                print(row)
```

**Metadata and page count** with `pypdf`:

```python
from pypdf import PdfReader

reader = PdfReader("input/document.pdf")
print(f"Pages: {len(reader.pages)}")
print(f"Title: {reader.metadata.title}")
```

### 4. Render PDF pages to PNG for visual review

```bash
pdftoppm -png -r150 input/document.pdf tmp/pdfs/pages
# Produces: tmp/pdfs/pages-1.png, tmp/pdfs/pages-2.png, ...
```

Options:
- `-r150` — 150 DPI (use `-r300` for high-quality, `-r72` for quick preview)
- `-png` — output as PNG (alternatives: `-jpeg`, `-tiff`)
- `-f 1 -l 3` — render only pages 1 through 3
- `-singlefile` — omit page numbers from output filename

### 5. Verify the final PDF

1. **Render to PNG** (Step 4) and visually inspect each page
2. **Extract text** (Step 3) to confirm content is readable and not garbled
3. **Check metadata** with `pypdf` — verify page count and title
4. **Validate structure** — open the PDF in a viewer to confirm links, bookmarks, and forms work

## Temp and Output Conventions

- Use `tmp/pdfs/` for intermediate rendered files; delete when done
- Write final artifacts under `output/pdf/`
- Keep filenames stable and descriptive (e.g., `invoice-2026-05.pdf`, not `output1.pdf`)

## Pitfalls

- **Missing fonts produce blank or garbled text**: Always register non-standard TTF fonts with `reportlab.pdfmetrics.registerFont()` before use. If you see empty rectangles or missing characters, the font isn't embedded.
- **Unicode encoding errors**: reportlab's default fonts only support Latin-1. For Unicode (CJK, emoji, accented chars), register a Unicode TTF font (e.g., Noto Sans) and use `Paragraph` from `reportlab.platypus`.
- **Layout shifts between platforms**: Font rendering differs across OSes. Use only embedded TTF fonts or stick to the 14 built-in PDF fonts for predictable results.
- **pdfplumber returns None**: `extract_text()` returns `None` on scanned/image-based PDFs. These need OCR first (e.g., `tesseract` via `pytesseract`), not text extraction.
- **Poppler not installed**: `pdftoppm` requires the `poppler-utils` system package. If missing, rendering fails with "command not found".
- **Large PDFs and memory**: `pdfplumber` loads entire files into memory. For PDFs over 100 pages, process pages in batches or use `pypdf` which streams pages.
- **Non-breaking hyphens (U+2011)**: These can cause rendering artifacts. Use ASCII hyphens (`-`) in reportlab text.
- **Page size mismatch**: Always specify `pagesize` when creating a `canvas.Canvas` or `SimpleDocTemplate`. The default is A4 — if you expect letter, set it explicitly.
- **Image distortion**: When placing images in reportlab, maintain the correct aspect ratio. Calculate width/height from the image dimensions rather than stretching.

## Verification

1. Confirm the PDF was created:
   ```bash
   test -f "output/pdf/report.pdf" && echo "PDF exists" || echo "PDF missing"
   ```
2. Confirm page count matches expectations:
   ```bash
   python3 -c "from pypdf import PdfReader; r=PdfReader('output/pdf/report.pdf'); print(f'Pages: {len(r.pages)}')"
   ```
3. Confirm pages render without errors:
   ```bash
   pdftoppm -png -r72 output/pdf/report.pdf /dev/null 2>&1 | head -5
   # No output = success; errors indicate rendering problems
   ```
4. Spot-check extracted text matches expected content:
   ```bash
   python3 -c "import pdfplumber; pdf=pdfplumber.open('output/pdf/report.pdf'); print(pdf.pages[0].extract_text()[:200])"
   ```

## Cross-References

- **screenshot** (`monitoring/screenshot`) — For capturing screen content that needs to be included in a PDF