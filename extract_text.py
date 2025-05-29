import os
from unstructured.partition.auto import partition

def extract_text_from_file(filepath: str) -> str:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    try:
        elements = partition(filename=filepath)
        text_content = "\n".join([el.text for el in elements if el.text])
        return text_content
    
    except Exception as e:
        raise RuntimeError(f"Failed to extract text: {e}")
