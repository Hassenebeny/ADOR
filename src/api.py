# src/api.py

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import os
import uvicorn

from parsers import parse_document
from ner import extract_financial_entities
from rag import rag_pdf_entity_extraction, rag_pdf_extraction
from rule_based import rule_based_extraction

app = FastAPI(
    title="Document Reader API",
    description="API pour uploader des documents et lancer divers traitements (NER, extraction rule-based, RAG/Q&A, résumé, extraction d'entités)"
)


@app.post("/process")
async def process_file(
    operation: str = Form(...),
    question: str = Form(None),
    llm_api_key: str = Form(None),
    file: UploadFile = File(...)
):
    """
    Endpoint permettant de traiter un document uploadé.

    - operation : type de traitement souhaité.
         Pour les PDF, les valeurs possibles sont :
            "qa" pour Q&A,
            "summarization" pour résumé,
            "entity_extraction" pour extraction d'entités.
         Pour les autres types, cette valeur n'est pas utilisée.
    - question : facultatif, utilisé pour Q&A sur PDF.
    - llm_api_key : facultatif, clé API Groq pour interroger le modèle via Langchain.
    - file : le document à traiter.

    Traitement par type de document :
      • DOCX : extraction rule-based (table ou paragraphes)
      • TXT : extraction NER customisée pour les chats
      • PDF : traitement via RAG avec Langchain et Groq, selon l'opération.
    """
    # Sauvegarde temporaire du fichier uploadé
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    ext = file.filename.split('.')[-1].lower()
    result = {}

    if ext in ["docx", "doc"]:
        # Pour les DOCX, on passe directement le chemin pour accéder aux tableaux
        result = rule_based_extraction(temp_file_path)
        result["process"] = "rule_based_extraction"
    elif ext == "txt":
        # Pour les TXT, on lit le texte et on utilise la fonction d'extraction NER customisée
        text = parse_document(temp_file_path)
        result = extract_financial_entities(text)
    elif ext == "pdf":
        # Pour les PDF, on lit le texte
        pdf_text = parse_document(temp_file_path)
        if llm_api_key:
            # Utilisation du pipeline RAG avec Groq via Langchain
            result = rag_pdf_entity_extraction(pdf_text, llm_api_key, operation, question)
            result["process"] = f"rag_{operation.lower()}"
        else:
            # Sinon, traitement de fallback
            result = rag_pdf_extraction(pdf_text)
            result["process"] = "rag_fallback"
    else:
        os.remove(temp_file_path)
        return JSONResponse(status_code=400, content={"error": "Type de fichier non supporté."})
    
    os.remove(temp_file_path)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
