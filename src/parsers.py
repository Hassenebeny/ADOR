
### 3. Le module `parsers.py`

# src/parsers.py

import os
import logging
from PyPDF2 import PdfReader
import docx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_pdf(file_path):
    """Extrait le texte d'un fichier PDF."""
    text = ""
    try:
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        logger.error(f"Erreur lors du parsing du PDF {file_path}: {e}")
    return text

def parse_docx(file_path):
    """Extrait le texte d'un fichier DOCX."""
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        logger.error(f"Erreur lors du parsing du DOCX {file_path}: {e}")
    return text

def parse_txt(file_path):
    """Extrait le texte d'un fichier TXT."""
    text = ""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        logger.error(f"Erreur lors du parsing du TXT {file_path}: {e}")
    return text

def parse_document(file_path):
    """Détecte le type de fichier et appelle le parser approprié."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return parse_pdf(file_path)
    elif ext in [".docx", ".doc"]:
        return parse_docx(file_path)
    elif ext == ".txt":
        return parse_txt(file_path)
    else:
        logger.error(f"Format de fichier non supporté: {ext}")
        return ""
