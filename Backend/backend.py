import chromadb
import pandas as pd
import torch
import nltk
import re
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain_chroma import Chroma
from chromadb.config import Settings
from nltk.corpus import stopwords


class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]
    model: str
    temperature: float


app = FastAPI()
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", model_kwargs={"device": "cpu"})


def clean_text(prompt):
  stop_words = set(stopwords.words("spanish"))
  texto_limpio = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ ]', ' ', prompt).lower()    
  word_set = set(texto_limpio.split() )
  keywords = [word for word in word_set if word not in stop_words]
  where_document = {
    "$or": [{"$contains": keyword} for keyword in keywords]
  }

  return where_document



def recuperacion(query):
    persist_directory = "./db"  # Especifica la ruta donde se almacenarán los datos
    client = chromadb.PersistentClient(path=persist_directory)
    collection_name = "news_ayacucho"

    try:
        collection = client.get_collection(collection_name)
        print(f"Conectado a la colección existente: {collection_name}")
    except Exception:
        
        collection = client.create_collection(collection_name)
        print(f"Se creó la colección: {collection_name}")

    query_embedding = embedding_model.embed_documents([query])[0]  

    results = collection.query(
        query_embeddings=[query_embedding],  
        n_results=6, 
        where_document = clean_text(query)
    )

    
    documents = results["documents"][0]  
    metadatas = results["metadatas"][0]  
    
    combined_text = "\n\n".join(
        f"Noticia: {doc.strip()}\nMetadatos: {', '.join(f'{key}: {value}' for key, value in meta.items())}"
        for doc, meta in zip(documents, metadatas)
    )
    #print(combined_text)

    return combined_text



@app.post("/chat/")
async def chat(request: ChatRequest):
    try:
        # Conecta con OpenAI o tu modelo local aquí
        #openai.api_key = "tu-clave-aqui"
        
        msg =[{"role": msg.role, "content": msg.content} for msg in request.messages]
       
        user_message = msg[-1]["content"] if msg else "No hay mensaje"
        recovered_context=recuperacion(user_message)

        if recovered_context:
            
            msg.append({"role": "system", "content": "la informacion recuperada son noticias "+recovered_context})
        else:
            msg.append({"role": "system", "content": "menciona que no encontraste las noticias solicitadas"})

        openai_client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
        response = openai_client.chat.completions.create(  
            model="local-model",  
            messages=msg,
            temperature=request.temperature
        )


        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}


