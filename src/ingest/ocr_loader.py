from PIL import Image
import pytesseract
from .base_extractor import BaseExtractor

class OCRExtractor(BaseExtractor):
    def __init__(self):
        super().__init__()
        
    def extract(self, file_path: str) -> str:
        is_valid_file_path = self.validate(file_path)
        if not is_valid_file_path:
            raise FileNotFoundError(f"File not found {file_path}")
        
        try:
            image = Image.open(file_path)
            image = image.convert("L")
            extracted_text = pytesseract.image_to_string(image, config="--psm 6")
            return extracted_text.strip()
        except Exception as e:
            raise ValueError(f"Unable to open image {file_path}: {e}")
        
if __name__ == "__main__":
    extractor = OCRExtractor()
    path = "data/raw/sample.jpg"
    result = extractor.extract(path)
    print(result)
        