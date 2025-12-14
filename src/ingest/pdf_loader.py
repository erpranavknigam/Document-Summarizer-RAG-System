import pypdf
import pdf2image
import pytesseract
from .base_extractor import BaseExtractor

class PDFExtractor(BaseExtractor):
    def __init__(self, use_ocr = False):
        super().__init__()
        self.use_ocr = use_ocr
        
    def extract(self, file_path: str) -> str:
        is_validated = super().validate(file_path)
        if not is_validated:
            raise FileNotFoundError(f"File not found")
        
        extracted_text = ""
        reader = pypdf.PdfReader(file_path)
        pages = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                pages.append(page_text.strip())
        extracted_text = "\n".join(pages)
        
        if self.use_ocr and len(extracted_text.strip()) < 50:
            extracted_text = self._ocr_pdf(file_path)
        return extracted_text
    
    def _ocr_pdf(self, file_path: str) -> str:
        is_validated = super().validate(file_path)
        if not is_validated:
            raise FileNotFoundError(f"File not found")
        
        images = pdf2image.convert_from_path(file_path, dpi=300)
        pages = []
        
        for page in images:
            if page:
                result = pytesseract.image_to_string(page)
                pages.append(result.strip())
        text_to_return = "\n".join(pages)
        return text_to_return
    
if __name__ == "__main__":
    extractor = PDFExtractor(use_ocr=True)
    file_path = "data/raw/sample.pdf"
    
    text = extractor.extract(file_path)
    print(text[:500])