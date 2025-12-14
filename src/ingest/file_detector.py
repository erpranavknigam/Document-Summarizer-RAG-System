import os
from dataclasses import dataclass

@dataclass
class FileInfo:
    path: str
    extension: str
    type: str | None
    is_supported: bool


class FileDetector:
    SUPPORTED_TYPES = {
        ".pdf": "pdf",
        ".docx": "docx",
        ".xlsx": "xlsx",
        ".xls": "xls",
        ".txt": "txt",
        ".png": "png",
        ".jpg": "jpg",
        ".jpeg": "jpeg"
    }

    def __init__(self):
        pass

    def detect(self, file_path: str) -> FileInfo:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        file_type = self.SUPPORTED_TYPES.get(ext, None)
        
        return FileInfo(
            path= file_path,
            extension=ext,
            type=file_type,
            is_supported=file_type is not None
        )


if __name__ == "__main__":
    detector = FileDetector()
    info = detector.detect("data/raw/sample.pdf")
    print(info)
