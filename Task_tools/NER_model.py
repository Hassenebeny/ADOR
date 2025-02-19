import spacy


def charger_texte(fichier):
    """Lit le contenu d'un fichier texte."""
    with open(fichier, "r", encoding="utf-8") as f:
        return f.read()

def extraire_entites(texte):
    """
    Charge le modèle NER généraliste spaCy et extrait les entités du texte.
    Retourne une liste de tuples (entité, label).
    """
    # Chargement du modèle NER (généraliste)
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(texte)
    entites = [(ent.text, ent.label_) for ent in doc.ents]
    return entites

if __name__ == "__main__":
    fichier = "data/FR001400QV82_AVMAFC_30Jun2028.txt"
    texte = charger_texte(fichier)
    entites = extraire_entites(texte)
    
    print("Entités extraites par le modèle NER :")
    for ent in entites:
        print(ent)
