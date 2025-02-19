import json
import docx

def extraire_donnees_docx(docx_path):
    """
    Extrait les paires clé/valeur du fichier DOCX.
    On récupère à la fois le contenu des paragraphes et des tableaux.
    """
    doc = docx.Document(docx_path)
    donnees = {}

    # Extraction depuis les paragraphes (en considérant que les clés et valeurs se suivent)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    # On parcourt par pas de 2 (clé, valeur)
    i = 0
    while i < len(paragraphs) - 1:
        cle = paragraphs[i]
        valeur = paragraphs[i + 1]
        if cle not in donnees:
            donnees[cle] = valeur
        i += 2

    # Extraction depuis les tableaux
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
    À partir du dictionnaire complet, on ne retient que les entités ciblées.
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

    # Dictionnaire de correspondance entre entités à extraire et mots-clés possibles dans le docx
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

if __name__ == "__main__":
    # Chemin du fichier DOCX
    docx_path = "data/ZF4894_ALV_07Aug2026_physical.docx"
    
    # Extraction brute du docx
    donnees = extraire_donnees_docx(docx_path)
    
    # Extraction des champs ciblés
    champs_extraits = extraire_champs(donnees)
    
    # Structure finale du JSON
    output = {
        "docx file": docx_path,
        "Entities to extract": champs_extraits
    }
    
    # Enregistrement dans un fichier JSON
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    
    # Affichage du résultat
    print(json.dumps(output, ensure_ascii=False, indent=4))
