# src/rag.py

import logging
from langchain_groq import ChatGroq  # Supposé disponible dans Langchain
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def rag_pdf_entity_extraction(text, api_key, operation, question=None):
    """
    Pipeline RAG pour les PDF utilisant Langchain et le modèle Groq.
    Selon l'opération demandée, le pipeline effectue l'une des actions suivantes :
      - "qa" : répondre à la question fournie à partir du document
      - "summarization" : fournir un résumé concis du document
      - "entity_extraction" : extraire les entités financières au format JSON
    Si aucune opération valide n'est spécifiée, un résumé par défaut est retourné.
    """
    # Initialisation du LLM Groq avec la clé API
    groq_llm = ChatGroq(groq_api_key=api_key, model_name="llama3-8b-8192", temperature=0, max_tokens=6000)
    
    if operation.lower() == "qa" and question:
        prompt_template = PromptTemplate(
            input_variables=["text", "question"],
            template=(
                "Vous êtes un expert en finance. Basé sur le texte suivant extrait d'un document financier, "
                "répondez à la question : '{question}'.\n\nTexte du document :\n{text}"
            )
        )
        inputs = {"text": text, "question": question}
    elif operation.lower() == "summarization":
        prompt_template = PromptTemplate(
            input_variables=["text"],
            template=(
                "Vous êtes un expert en lecture de documents financiers. Veuillez fournir un résumé concis du texte suivant :\n\n{text}"
            )
        )
        inputs = {"text": text}
    elif operation.lower() == "entity_extraction":
        prompt_template = PromptTemplate(
            input_variables=["text"],
            template=(
                "Vous êtes un expert en extraction d'entités financières. Extraites les entités suivantes au format JSON "
                "(clés : Counterparty, Notional, ISIN, Underlying, Maturity, Bid, Offer, PaymentFrequency) à partir du texte suivant :\n\n{text}"
            )
        )
        inputs = {"text": text}
    else:
        # Par défaut, résumé
        prompt_template = PromptTemplate(
            input_variables=["text"],
            template=(
                "Vous êtes un expert en lecture de documents financiers. Veuillez fournir un résumé concis du texte suivant :\n\n{text}"
            )
        )
        inputs = {"text": text}

    chain = LLMChain(llm=groq_llm, prompt=prompt_template)
    try:
        result_text = chain.run(inputs)
        logger.info("Réponse LLM obtenue via Groq.")
    except Exception as e:
        logger.error(f"Erreur lors de l'appel au modèle Groq via Langchain : {e}")
        result_text = f"Erreur lors de l'appel au modèle Groq : {e}"
    
    return {"rag_result": result_text}

def rag_pdf_extraction(text):
    """
    Fonction de fallback sans LLM. Retourne un résumé basé sur les 200 premiers caractères du document.
    """
    summary = text[:200] + "..." if len(text) > 200 else text
    return {"rag_summary": summary}
