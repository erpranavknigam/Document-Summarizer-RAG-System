import os
from abc import ABC, abstractmethod
class BaseExtractor(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def extract(self, file_path: str) -> str:
        pass
        
    def validate(self, file_path: str) -> bool:
        if not os.path.exists(file_path):
            return False
        return True