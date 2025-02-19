import json
import docx

def extraire_donnees_docx(docx_path):
    """
    Extrait les paires clé/valeur du fichier DOCX.
    Récupère à la fois le contenu des paragraphes et des tableaux.
    Retourne un dictionnaire contenant toutes les paires extraites.
    """
    doc = docx.Document(docx_path)
    donnees = {}

    # Extraction depuis les paragraphes (en considérant que les clés et valeurs se suivent)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    i = 0
    while i < len(paragraphs) - 1:
        cle = paragraphs[i]
        valeur = paragraphs[i + 1]
        # On stocke la première occurrence de la clé
        if cle not in donnees:
            donnees[cle] = valeur
        i += 2

    # Extraction depuis les tableaux : pour chaque ligne avec au moins 2 cellules
    for table in doc.tables:
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
            if len(cells) >= 2:
                cle = cells[0]
                valeur = cells[1]
                donnees[cle] = valeur

    return donnees

def extraire_champs(donnees):
    """
    À partir du dictionnaire complet, conserve uniquement les entités ciblées.
    La correspondance se fait par recherche de mots-clés (non sensible à la casse).
    """
    result = {}

    # Extraction du Counterparty : on recherche uniquement "Party A"
    counterparty = None
    for key, value in donnees.items():
        if "party a" in key.lower():
            counterparty = value
            break
    result["Counterparty"] = counterparty

    # Dictionnaire de correspondance entre entités à extraire et mots-clés possibles
    mapping = {
        "Initial Valuation Date": ["Initial Valuation Date"],
        "Notional": ["Notional", "Notional Amount"],
        "Valuation Date": ["Valuation Date"],
        "Maturity": ["Termination Date", "Maturity Date"],
        "Underlying": ["Underlying"],
        "Coupon": ["Coupon"],
        "Barrier": ["Barrier"],
        "Calendar": ["Business Day", "Calendar"]
    }

    for champ, keywords in mapping.items():
        valeur_trouvee = None
        for mot in keywords:
            for key, value in donnees.items():
                if mot.lower() in key.lower():
                    valeur_trouvee = value
                    break
            if valeur_trouvee:
                break
        result[champ] = valeur_trouvee

    return result

def rule_based_extraction(file_path):
    """
    Fonction d'extraction rule-based adaptée pour l'API.
    Ouvre le document DOCX situé à file_path, extrait les données brutes,
    sélectionne les champs ciblés et renvoie une structure de données exploitable.
    """
    donnees = extraire_donnees_docx(file_path)
    champs_extraits = extraire_champs(donnees)
    output = {
        "docx file": file_path,
        "Entities to extract": champs_extraits
    }
    return output
