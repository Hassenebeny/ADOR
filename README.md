# ADOR
 build a financial document reader tool  augmented by IA
## GAD and GMD :
You will find a docx file that explains the global architecture and a global methdology document that explains both NER model fine-tuning and the role of RAG/LLM in an entity recognition use case.

# Coding Games : /Task_tools
## Requirements 
```bash
pip install -r requirements.txt
```
## Rule Based
```bash
python Task_tools/rule_based_rec.py
```
It will take the file docx in data and do the rule based algorithm to find entities keys and values corresponding.

## NER Model
```bash
python Task_tools/rule_based_rec.py
```
It will take a text document in data folder and download a NER model then it will find the entities from text.

# Fastapi 
API for document upload and processing (NER, rule-based extraction, RAG/Q&A, summary, entity extraction)
```bash
python src/api.py
```
It will open an https link to connect to the API. In the API you can try a process request.
In process, you put your file, if it is txt or docs, it will do both task (NER Model and rule based).
If you put a pdf file, you have to mention eather "qa" , "summarization" or "entity_extraction" to do a little prompt engineering and LLMs generation of text from tha pdf file.
You will need a Groq API KEY to use LLama model from : https://console.groq.com/keys

