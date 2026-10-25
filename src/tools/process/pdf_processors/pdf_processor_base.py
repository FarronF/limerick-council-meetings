from abc import ABC, abstractmethod

from tools.logging.file_logger import FileLoggerSingleton


class PdfProcessorBase(ABC):
    def log_ocr_usage(self, pdf_path: str):
        """Log the use of OCR for a PDF."""
        FileLoggerSingleton._instance.log("ocr_used", pdf_path)

    @abstractmethod
    def process(self, pdf_path: str):
        """Process a PDF and return its extracted text."""
        pass
