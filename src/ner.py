# src/ner.py

import spacy
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_financial_entities(texte):
    """
    Charge le modèle NER généraliste spaCy et extrait les entités du texte.
    Retourne une liste de tuples (entité, label).
    """
    # Chargement du modèle NER (généraliste)
    try:
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(texte)
        entites = [(ent.text, ent.label_) for ent in doc.ents]
    except Exception as e:
        logger.error(f"Erreur lors du chargement du modèle {"en_core_web_sm"}: {e}")
        raise e    

    return entites
