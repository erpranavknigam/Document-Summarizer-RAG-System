import openpyxl
from .base_extractor import BaseExtractor

class ExcelExtractor(BaseExtractor):
    def __init__(self):
        super().__init__()
        
    def extract(self, file_path: str) -> str:
        is_valid_file = super().validate(file_path)
        if not is_valid_file:
            raise FileNotFoundError(f"File not found {file_path}")
        
        reader = openpyxl.load_workbook(file_path, data_only=True)
        sheet_data = []
        for sheet in reader.worksheets:
            row_data = []
            for row in sheet.rows:
                cell_data = []
                for cell in row:
                    cell_value = str(cell.value).strip() if cell.value is not None else " "
                    cell_data.append(cell_value)
                cell_extracted_text = "|".join(cell_data)
                row_data.append(cell_extracted_text.strip())
            row_extracted_text =  f"Sheet: {sheet.title}\n" + "\n".join(row_data)
            sheet_data.append(row_extracted_text)
        extracted_text = "\n\n".join(sheet_data)
        return extracted_text
    
if __name__ == "__main__":
    extractor = ExcelExtractor()
    path = "data/raw/sample.xlsx"
    result = extractor.extract(path)
    print(result[:500])
                