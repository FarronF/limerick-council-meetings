import re

from markdownify import markdownify
from PIL import Image
import fitz
import pytesseract

from tools.process.pdf_processors.pdf_processor_base import PdfProcessorBase


class FitzProcessor(PdfProcessorBase):
    def process(self, pdf_path: str):
        """Extract text from a PDF, using OCR for scanned pages."""
        doc = fitz.open(pdf_path)
        markdown_output = ""
        ocr_used = False
        for page_num in range(len(doc)):
            page = doc[page_num]

            if not page.get_text().strip():
                if not ocr_used:
                    self.log_ocr_usage(pdf_path)
                    ocr_used = True
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img = img.resize(
                    (pix.width * 3, pix.height * 3), Image.Resampling.LANCZOS
                )
                ocr_text = pytesseract.image_to_string(img)
                markdown_output += (
                    "*<small>Scanned page, text may contain errors. "
                    "See original file for clarity</small>*  \n\n"
                    f"{ocr_text}\n"
                )
            else:
                html_text = page.get_text("html")
                html_text = re.sub(r"<img[^>]*>", "(Image omitted)", html_text)
                markdown_output += markdownify(html_text)
            markdown_output += f"\n\n[[PAGE_END:{page_num + 1}]]\n\n"

        return re.sub(r"\*\*\*\*", "", markdown_output)
