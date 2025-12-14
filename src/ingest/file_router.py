from .file_detector import FileDetector
from .pdf_loader import PDFExtractor
from .docx_loader import DOCXExtractor
from .excel_loader import ExcelExtractor
from .ocr_loader import OCRExtractor
import os

class ExtractorRouter:
    def __init__(self):
        pass

    def get_extractor(self, file_path: str):
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_detector = FileDetector()
        file_data = file_detector.detect(file_path)

        if file_data is None or not file_data.is_supported:
            raise ValueError(f"Unsupported or invalid file: {file_path}")

        extension_map = {
            ".pdf": PDFExtractor,
            ".docx": DOCXExtractor,
            ".xlsx": ExcelExtractor,
            ".jpg": OCRExtractor,
            ".jpeg": OCRExtractor,
            ".png": OCRExtractor
        }

        ExtractorClass = extension_map.get(file_data.extension.lower())
        if ExtractorClass is None:
            raise ValueError(f"Unsupported file extension: {file_data.extension}")

        if file_data.extension.lower() == ".pdf":
            return ExtractorClass(use_ocr=True)

        return ExtractorClass()


if __name__ == "__main__":
    router = ExtractorRouter()
    file_path = "data/raw/sample.pdf"
    extractor = router.get_extractor(file_path)
    text = extractor.extract(file_path)
    print(text[:500])
